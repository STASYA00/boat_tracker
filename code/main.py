import argparse
import textwrap

from pipeline import Yolo5DeepSortPipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description=textwrap.dedent('''\
			USAGE: python3 main.py --source 1.mp4

	        ------------------------------------------------------------------------
	
	        Boat detection app combining Yolo object detection and DeepSort tracking.
            Writes out a video file with the result of the detection.
	
	        ------------------------------------------------------------------------
	
	        --source        video file for boat detection, str
	
	        ------------------------------------------------------------------------
	
	        '''), epilog=textwrap.dedent('''\
	        The algorithm will be updated.
	        '''))
            
    parser.add_argument('--source', type=str, help='path to the video file'
                                                    ', str')

	############################################################################
     
    args = parser.parse_args()
    
    pipe = Yolo5DeepSortPipeline(args.source, write=True, show=False)
    pipe.run()