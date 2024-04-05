import dpfp
import dpfp.fingerprints
import dpfp.io
import dpfp.processing
import dpfp.sensor
import dpfp.feature
from dpfp import VerificationStatus

def capture_fingerprint():
    try:
        with dpfp.sensor.Capture() as capturer:
            print("Place your finger on the sensor...")
            while True:
                raw_sample = capturer.read()
                sample = dpfp.processing.normalize(raw_sample)
                
                if raw_sample is not None:
                    print("Fingerprint captured successfully!")
                    return sample.serialize()
    
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    fingerprint_data = capture_fingerprint()
    if fingerprint_data:
        print("Fingerprint data:", fingerprint_data)
