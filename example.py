import DiMo2d
import sys


def test_2d_func():
    likelihood_dir = sys.argv[1]
    binary_dir = sys.argv[2]
    morse_dir = sys.argv[3]
    json_dir = sys.argv[4]

    # These settings are for practical examples like the ones that can be found in /data/PMD-likelihood
    # For the synthetic test cases, the recommended parameters are the ones commented out below
    ve_thresh = 0 # 0
    et_thresh = 64 # 0

    threads = 1 # 1
    bit_depth = 8 # 16
    background_pixel_val = 31 # 0

    DiMo2d.compute_persistence_single_channel(likelihood_dir, morse_dir, threads, bit_depth, background_pixel_val)
    DiMo2d.generate_morse_graphs(morse_dir, binary_dir, ve_thresh, et_thresh, threads)
    DiMo2d.postprocess_graphs(morse_dir, ve_thresh, et_thresh, threads)
    # DiMo2d.cshl_post_results(morse_dir, json_dir, ve_thresh, et_thresh, threads)


if __name__ == '__main__':
    test_2d_func()

