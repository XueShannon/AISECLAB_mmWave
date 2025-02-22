classdef (StrictDefaults) hNRPhaseNoise < matlab.System
    % hNRPhaseNoise Apply phase noise to a complex baseband signal, as
    % defined in TR 38.803.
    %
    % PHNOISE = hNRPhaseNoise creates a phase noise System object, PHNOISE.
    %   This object applies phase noise to a complex baseband signal, as
    %   defined in TR 38.803.
    %
    %   PHNOISE = hNRPhaseNoise(Name=Value) creates a phase noise object,
    %   PHNOISE, with the specified property Name set to the specified Value.
    %   You can specify additional name-value pair arguments in any order as
    %   (Name1=Value1,...,NameN=ValueN).
    %
    %   PHNOISE = hNRPhaseNoise(CARRIERFREQUENCY,SAMPLERATE,Name=Value)
    %   creates a phase noise object, PHNOISE, with the CarrierFrequency
    %   property set to CARRIERFREQUENCY, the SampleRate property set to
    %   SAMPLERATE, and other specified property Names set to the specified
    %   Values. CARRIERFREQUENCY and SAMPLERATE are value-only arguments.
    %   To specify a value-only argument, you must also specify all
    %   preceding value-only arguments. You can specify name-value pair
    %   arguments in any order.
    %
    %   Step method syntax:
    %
    %   Y = step(PHNOISE,X) adds phase noise to the input X and returns the
    %   result in Y. X must be a N-by-1 vector or N-by-M matrix with data
    %   type double or single, where N is number of samples and M is number
    %   of radio frequency chains. The step method outputs, Y, as a
    %   complex-valued signal with the same data type and size as the
    %   input.
    %
    %   System objects may be called directly like a function instead of using
    %   the step method. For example, y = step(obj, x) and y = obj(x) are
    %   equivalent.
    %
    %   hNRPhaseNoise methods:
    %
    %   step      - Apply phase noise to input signal (see above)
    %   release   - Allow property value and input characteristics changes
    %   clone     - Create phase noise object with same property values
    %   isLocked  - Locked status (logical)
    %   visualize - Plot response of phase noise filter
    %
    %   hNRPhaseNoise properties:
    %
    %   CarrierFrequency   - Carrier frequency (Hz)
    %   MinFrequencyOffset - Minimum frequency offset (Hz)
    %   Model              - Phase noise model
    %   SampleRate         - Sample rate (Hz)
    %   RandomStream       - 'Global stream' or 'mt19937ar with seed'
    %   Seed               - Initial seed
    %
    %   See also comm.PhaseNoise, comm.PhaseFrequencyOffset

    %   Copyright 2024 The MathWorks, Inc.

    %#codegen

    % Public, non-tunable properties
    properties (Nontunable)
        %CarrierFrequency Carrier frequency (Hz)
        %   Specify the carrier frequency in Hz as a positive, real scalar
        %   of data type double. The default is 30 GHz.
        CarrierFrequency (1,1) {mustBeDbl(CarrierFrequency), mustBePositive} = 30e9
        %MinFrequencyOffset Minimum frequency offset (Hz)
        %   Specify the minimum frequency offset in Hz as a positive, real
        %   scalar of data type double. The phase noise power spectral
        %   density between MinFrequencyOffset and SampleRate/2 is defined
        %   in TR 38.803. The phase noise has 1/f^3 characteristics below
        %   MinFrequencyOffset. A lower value of MinFrequencyOffset more
        %   accurately models the low frequency phase noise of TR 38.803
        %   but results in a longer time to design the phase noise filter.
        %   The default is 1 KHz.
        MinFrequencyOffset (1,1) {mustBeDbl(MinFrequencyOffset), mustBePositive} = 1e3
        %Model Phase noise model
        %   Specify the phase noise model to use from TR 38.803 as one of
        %   '29.55', '45', '70' or 'Auto'. Specify '29.55', '45' or '70' to
        %   use the parameters for model operating at 29.55 GHz, 45 GHz and
        %   70 GHz respectively. 'Auto' uses the model nearest to the
        %   specified CarrierFrequency. The default is 'Auto'.
        Model (1,:) char {matlab.system.mustBeMember(Model, {'Auto','29.55','45','70'})} = 'Auto';
        %SampleRate Sample rate (Hz)
        %   Specify the sample rate in samples per second as a positive,
        %   real scalar of data type double. The default is 100 MHz.
        SampleRate (1,1) {mustBeDbl(SampleRate), mustBePositive} = 100e6
        %RandomStream Random number source
        %   Specify the source of random number stream as one of 'Global
        %   stream' | 'mt19937ar with seed'.  If RandomStream is set to
        %   'Global stream', the current global random number stream is
        %   used for normally distributed random number generation.  If
        %   RandomStream is set to 'mt19937ar with seed', the mt19937ar
        %   algorithm is used for normally distributed random number
        %   generation, in which case the reset method reinitializes the
        %   random number stream to the value of the Seed property. The
        %   default value of this property is 'Global stream'.
        RandomStream (1,:) char {matlab.system.mustBeMember(RandomStream, {'Global stream', 'mt19937ar with seed'})} = 'Global stream';
        %Seed Initial seed
        %   Specify the seed as a positive double precision integer-valued
        %   scalar less than 2^32. The default is 2137. This property is
        %   relevant when the RandomStream property is set to 'mt19937ar
        %   with seed'.
        Seed (1,1) {mustBeDbl(Seed), mustBePositive} = 2137
    end

    properties (Access = private, Nontunable)
        pPN % comm.PhaseNoise
    end

    methods
        function obj = hNRPhaseNoise(varargin)
            % 'CarrierFrequency' & 'SampleRate' are value-only arguments.
            setProperties(obj,nargin,varargin{:},'CarrierFrequency', 'SampleRate');
        end

        function varargout = visualize(obj)
            nargoutchk(0, 1);
            if ~obj.isLocked
                setupPN(obj);
            end
            hFigure = obj.pPN.visualize();
            % Delete 'Specified PSD' line as it is not relevant
            hls = findobj(hFigure, 'Type','line', 'DisplayName', 'Specified PSD');
            delete(hls);
            % Compute and plot the PSD for the specified model
            hlr = findobj(hFigure, 'Type','line', 'DisplayName', 'Realized PSD');
            fVec = get(hlr, 'XData');
            lvlDb = getPhaseNoisePSD(obj, fVec);
            hAx = gca(hFigure);
            hold(hAx,'on');
            ln = semilogx(hAx, fVec, lvlDb, 'r-.');
            mdl = getModel(obj);
            % PSD is not scaled if the carrier frequency matches the model
            % base carrier frequency
            if any(obj.CarrierFrequency == [29.55, 45, 70]*1e9)
                displayName = [mdl ' GHz'];
            else
                displayName = [mdl ' GHz Scaled'];
            end
            ln.DisplayName = displayName;
            xLimits = get(hAx, 'XLim');
            xLimits(1) = max(xLimits(1), obj.MinFrequencyOffset);
            set(hAx, 'XLim', xLimits);
            hold(gca(hFigure),'off');
            if nargout == 1
                varargout{1} = hFigure;
            end
        end
    end

    methods (Access = protected)
        function setupImpl(obj)
            setupPN(obj);
        end

        function y = stepImpl(obj,u)
            y = obj.pPN(u);
        end

        function resetImpl(obj)
            reset(obj.pPN);
        end

        function releaseImpl(obj)
            release(obj.pPN);
        end

        function s = saveObjectImpl(obj)
            s = saveObjectImpl@matlab.System(obj);
            if isLocked(obj)
                s.pPN = matlab.System.saveObject(obj.pPN);
            end
        end

        function loadObjectImpl(obj,s,wasLocked)
            if wasLocked
                obj.pPN = matlab.System.loadObject(s.pPN);
            end
            loadObjectImpl@matlab.System(obj,s);
        end

        function validateInputsImpl(~,u)
            % Must be a scalar, a column vector or a matrix.
            % Only floating point numbers are supported.
            validateattributes(u,{'double','single'},{'2d'},'','X')
        end

        function flag = isInputSizeMutableImpl(~,~)
            flag = true;
        end

        function flag = isInactivePropertyImpl(obj,prop)
            flag = strcmp(prop, 'Seed') && strcmp(obj.RandomStream, 'Global stream');
        end
    end

    methods (Access = private)
        function setupPN(obj)
            % Setup comm.PhaseNoise

            fVec = logspace(log10(obj.MinFrequencyOffset), log10(obj.SampleRate/2)-0.001, 20);
            lvlDb = getPhaseNoisePSD(obj, fVec);

            obj.pPN = comm.PhaseNoise("FrequencyOffset",fVec, ...
                "Level",lvlDb,"SampleRate",obj.SampleRate);
            if strncmp(obj.RandomStream, 'm', 1)
                obj.pPN.RandomStream = 'mt19937ar with seed';
                obj.pPN.Seed = obj.Seed;
            end
        end

        function PN_dBcPerHz = getPhaseNoisePSD(obj, fVec)
            % Compute phase noise PSD for specified frequency offset fVec
            % (in Hz) as defined in TR 38.803

            mdl = getModel(obj);
            switch mdl
                case '29.55'
                    % Parameter set from TR 38.803 for 29.55 GHz Fc
                    fcBase = 29.55e9;
                    fz = [3e3 550e3 280e6];
                    fp = [1 1.6e6 30e6];
                    alphaz = [2.37 2.7 2.53];
                    alphap = [3.3 3.3 1];
                    PSD0 = 32;
                case '45'
                    % Parameter set from TR 38.803 for 45 GHz Fc
                    fcBase = 45e9;
                    fz = [3e3 451e3 458e6];
                    fp = [1 1.54e6 30e6];
                    alphaz = [2.37 2.7 2.53];
                    alphap = [3.3 3.3 1];
                    PSD0 = 35.65;
                otherwise
                    % Parameter set from TR 38.803 for 70 GHz Fc
                    fcBase = 70e9;
                    fz = [3e3 396e3 754e6];
                    fp = [1 1.55e6 30e6];
                    alphaz = [2.37 2.7 2.53];
                    alphap = [3.3 3.3 1];
                    PSD0 = 39.49;
            end

            % Compute numerator
            num = ones(size(fVec));
            for ii = 1:numel(fz)
                num = num.*(1 + (fVec./fz(ii)).^alphaz(ii));
            end

            % Compute denominator
            den = ones(size(fVec));
            for ii = 1:numel(fp)
                den = den.*(1 + (fVec./fp(ii)).^alphap(ii));
            end

            % Compute phase noise and apply a shift for carrier frequencies
            % different from the base frequency
            PN_dBcPerHz = 10*log10(num./den) + PSD0 + 20*log10(obj.CarrierFrequency/fcBase);
        end

        function mdl = getModel(obj)
            if strncmp(obj.Model, 'A', 1)
                [~,idx] = min(abs(obj.CarrierFrequency - [29.55, 45, 70]*1e9));
                validMdl = {'29.55','45','70'};
                mdl = validMdl{idx};
            else
                mdl = obj.Model;
            end
        end

    end

    methods (Hidden, Sealed)
        function freqOffset = getFrequencyOffset(obj)
            setupPN(obj);
            freqOffset = obj.pPN.FrequencyOffset;
        end

        function freqOffset = getLevel(obj)
            setupPN(obj);
            freqOffset = obj.pPN.Level;
        end
    end
end

function mustBeDbl(value)
    validateattributes(value, {'double'}, {});
end