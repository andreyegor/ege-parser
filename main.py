import parser_funcs
import data
import cv2
import asyncio
out = asyncio.run(parser_funcs.check(data=data.data, silent=False))
if out:
    cv2.imshow('image', cv2.imread(out['image']))
    cv2.waitKey(0)  
else:
    print(':(')