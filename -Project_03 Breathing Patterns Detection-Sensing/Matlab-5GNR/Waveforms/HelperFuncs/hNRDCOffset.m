function dcOffset = hNRDCOffset(carrier,waveConfig,rxWaveform,refGrid,cdmLengths,firstDmrsLocInSlot,sr,bwpIdx)
% hNRDCOffset DC offset estimation.
%   [DCOFFSET] =
%   hNRDCOffset(CARRIER,WAVECONFIG,RXWAVEFORM,REFGRID,CDMLENGTHS,DLFLAG,...
%                                             FIRSTDMRSLOCINSLOT,SR,BWPIDX)
%   returns a complex valued DC offset DCOFFSET corresponding to the input
%   RXWAVEFORM.
%   CARRIER             - Carrier configuration object, <a
%                         href="matlab:help('nrCarrierConfig')"
%                         >nrCarrierConfig</a>
%   WAVECONFIG          - Input structure or object of type
%                         <a href="matlab:help('nrDLCarrierConfig')"
%                         >nrDLCarrierConfig</a> or <a
%                         href="matlab:help('nrULCarrierConfig')"
%                         >nrULCarrierConfig</a>
%                         containing carrier and cell related parameters.
%   RXWAVEFORM          - T-by-R matrix where T is the number of time
%                         domain samples and R is the number of receive
%                         antennas
%   REFGRID             - Slot based grid containing known reference
%                         symbols of size K-by-L-by-P. K is the number of
%                         subcarriers, given by CARRIER.NSizeGrid * 12. L
%                         is the number of symbols spanning the duration of
%                         RXWAVEFORM. P is the number of reference signal
%                         ports.
%   CDMLENGTHS          - A 2-element row vector [FD TD] specifying the
%                         length of FD-CDM and TD-CDM despreading to
%                         perform.
%   FIRSTDMRSLOCINSLOT  - Symbol location of the first DMRS in slot
%   SR                  - Waveform sample rate
%   BWPIDX              - Bandwidth part index
%
%   The function subtracts the mean of the input RXWAVEFORM from the input
%   itself and subsequently creates a channel estimate which removes the
%   influence of the remaining DC offset. The channel estimate is then
%   applied to the known reference symbols in the input and generate the
%   corresponding time domain waveform. To reduce the impact of the
%   residual DC offset concentrated around the DC location, this region in
%   the channel estimate is removed and linearly interpolated. The
%   resulting channel estimate is close to the true channel estimate
%   without the influence of the DC offset.

% Copyright 2023 The MathWorks, Inc.

    % DC offset estimation of mean of the signal in time domain.
    dcOffset1 = mean(rxWaveform,'all');

    % Ignore very small DC offsets. The multiplier, 0.03, was chosen
    % heuristically
    if abs(dcOffset1) < 0.03*std(rxWaveform,1,'all')
        dcOffset = 0;
    else

        % DC offset correction in time domain
        rxWaveform = rxWaveform - dcOffset1;

        % Obtain waveform configuration parameters
        [~,winfo] = nrWaveformGenerator(waveConfig);
        k0 = winfo.ResourceGrids(bwpIdx).Info.k0;
        scs = carrier.SubcarrierSpacing;
        symbolsPerSlot = carrier.SymbolsPerSlot;
        k0Offset = k0*scs*1e3;

        % Demodulate the time domain waveform.
        rxGrid = nrOFDMDemodulate(carrier,rxWaveform,'SampleRate',sr,'CarrierFrequency',waveConfig.CarrierFrequency+k0Offset);
        gridSize = size(rxGrid);
        nSlots = floor(gridSize(2)/symbolsPerSlot);
        if nSlots > waveConfig.NumSubframes*carrier.SlotsPerSubframe
            waveConfig.NumSubframes = ceil(nSlots/carrier.SlotsPerSubframe);
            [~,winfo] = nrWaveformGenerator(waveConfig);
        end

        % Work only on the relevant BWP in the waveform to simplify indexing
        bwpCfg = waveConfig.BandwidthParts{bwpIdx};
        bwpStart = bwpCfg.NStartBWP-carrier.NStartGrid;
        rxGrid = rxGrid(12*bwpStart+1:12*(bwpStart+bwpCfg.NSizeBWP),:,:);

        refgridNoOffset = winfo.ResourceGrids(bwpIdx).ResourceGridInCarrier;
        if ~isempty(refGrid)
            refGrid = refGrid(12*bwpStart+1:12*(bwpStart+bwpCfg.NSizeBWP),:,:);
            refgridNoOffset = refgridNoOffset(12*bwpStart+1:12*(bwpStart+bwpCfg.NSizeBWP),:,:);
        end

        % Locate the DC subcarrier location for this bandwidth part
        % Adjust DC location based on BWP start
        dcIndCarrier = (carrier.NSizeGrid*12)/2+1-k0;
        dcInd = dcIndCarrier - bwpStart*12;

        % Skip DC offset estimation if DC location is outside this BWP
        if (dcInd < 1 || dcInd > size(refGrid,1))
            dcOffset = 0;
            return;
        end

        % Set channel estimate interpolation region
        dcOffsetLow = dcInd-3;
        dcOffsetHigh = dcInd+2;

        % Erase a portion of the reference grid around the DC
        refGrid(dcOffsetLow:dcOffsetHigh,:,:) = 0;
        
        % Estimate the channel
        % Set 'channelEstimateSmoothen' to enable smoothening of the
        % channel coefficients in the frequency domain, using a moving
        % average filter.
        channelEstimateSmoothen = 1;
        HestLow= hChannelEstEVM({rxGrid},refGrid,cdmLengths,symbolsPerSlot,channelEstimateSmoothen);
        
        % Modify the channel estimate by removing reference symbols near DC and then interpolating across them.
        % This removes the majority of the influence of the DC offset
        numSCs = size(rxGrid,1);
        R = size(HestLow,3);
        P = size(HestLow,4);
        for slotIdx = 1:nSlots
            symIdx = (slotIdx-1)*symbolsPerSlot+1:slotIdx*symbolsPerSlot;
            for p = 1:P
                for r = 1:R
                    H_tmp = HestLow(:,symIdx(firstDmrsLocInSlot),r,p);
                    if sum(H_tmp) == 0
                        continue;
                    end

                    % Obtain channel estimate coeeficients for all
                    % subcarriers by interpolating over know reference
                    % locations.
                    interpEqCoeff = interp1(find(H_tmp~=0),H_tmp(H_tmp~=0),(1:numSCs).','linear','extrap');

                    % Select two equidistant locations around DC
                    % Interpolate the channel across these two locations 
                    interpEqCoeffTemp = interp1(1:5:6,[interpEqCoeff(dcOffsetLow) interpEqCoeff(dcOffsetHigh)],1:6,'linear');

                    % Overwrite this interpolated section over the channel
                    % estimate. This is to remove the majority of the DC
                    % effect.
                    interpEqCoeff(dcOffsetLow:dcOffsetHigh,:) = interpEqCoeffTemp.';
                    interpEqCoeff(isnan(interpEqCoeff)) = 1e-9;
                    interpEqCoeff = repmat(interpEqCoeff,1,symbolsPerSlot);
                    HestLow(:,symIdx,r,p) = interpEqCoeff;
                end
            end
        end

        % Ensure Hest & refgridNoOffset are of same slot lengths
        refLen = size(refgridNoOffset,2);
        HestLen = size(HestLow,2);
        Hest = HestLow;
        if refLen < HestLen
            Hest = HestLow(:,1:refLen,:,:);
        end
        if HestLen < refLen
            refgridNoOffset = refgridNoOffset(:,end-HestLen+1:end,:,:);
        end

        % Create full carrier grids where BWP specific 'refgridNoOffset' and 'Hest'
        % will be inserted into.
        refgridNoOffsetFullCarrier = zeros(gridSize(1),floor(gridSize(2)/symbolsPerSlot)*symbolsPerSlot,size(HestLow,4));
        HestFullCarrier = refgridNoOffsetFullCarrier;
        refgridNoOffsetFullCarrier(12*bwpStart+1:12*(bwpStart+bwpCfg.NSizeBWP),:,1:size(refgridNoOffset,3)) = refgridNoOffset;
        HestFullCarrier(12*bwpStart+1:12*(bwpStart+bwpCfg.NSizeBWP),:,1) = Hest(:,:,1,1);
    
        % Create a reference waveform modulated with the channel estimate
        refWaveform = nrOFDMModulate(carrier,refgridNoOffsetFullCarrier.*HestFullCarrier(:,:,1,1));

        % Ensure reference and received waveform lengths match
        refLen = size(refWaveform,1);
        rxLen = size(rxWaveform,1);
        if refLen < rxLen
            refWaveform = [refWaveform; zeros((rxLen - refLen), size(refWaveform,2))];
        end
        if rxLen < refLen
            refWaveform(rxLen+1:end,:) = [];
        end

        % Estimate residual DC offset
        dcOffset2 = mean(rxWaveform - refWaveform,'all');

        % Combine the larger DC offset dcOffset1, with the residual DC offset,
        % dcOffset2
        dcOffset = dcOffset1 + dcOffset2;
    end
end