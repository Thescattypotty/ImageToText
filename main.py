import os
import pytesseract
from PIL import Image, ImageEnhance
from pytesseract import Output
import cv2
import numpy as np


def calculate_threshold(image_path):
    img = cv2.imread(image_path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    hist = cv2.calcHist([gray], [0], None, [256], [0,256])
    
    min_hist_index = np.argmin(hist[100:156]) + 100
    
    lower_threshold = int(min_hist_index)
    upper_threshold = 255
    
    return lower_threshold, upper_threshold

def extract_text(image_path, lang='eng'):
    try:
        img = Image.open(image_path)
                
        #lower_threshold, upper_threshold = calculate_threshold(image_path)
        gray = img.convert('L')
        img_np = np.array(gray)
        white_mask = cv2.inRange(img_np, 176, 255)
        
        img_filtered = cv2.bitwise_and(img_np, img_np, mask=white_mask)
        
        img_filtered_pil = Image.fromarray(img_filtered)
        
        text = pytesseract.image_to_string(img_filtered_pil, lang=lang)
        return text.strip()
    except FileNotFoundError:
        return "Image file not found"
    except Exception as e:
        return f"Error: {e}"
    
def post_process_text(text):
    import re
    text = re.sub(r'[^a-zA-Z0-9]', '', text)
    return text 

def calculate_accuracy(extracted_text, ground_truth_text):
    import re
    extracted_text_cleaned = re.sub(r'[^a-zA-Z0-9]', '', extracted_text.lower())
    ground_truth_text_cleaned = re.sub(r'[^a-zA-Z0-9]', '', ground_truth_text.lower())
    
    #matching_characters = sum(1 for x, y in zip(extracted_text_cleaned, ground_truth_text_cleaned) if x == y)
    matching_characters = sum(1 for char in extracted_text_cleaned if char in ground_truth_text_cleaned)
    
    accuracy = (matching_characters / len(ground_truth_text_cleaned)) * 100
    if len(extracted_text_cleaned) > len(ground_truth_text_cleaned):
        if accuracy > 100:
            accuracy=90
            
    return max(accuracy, 0)

if __name__ == "__main__":
    
    extracted_text = []
    image_files = [
        "AACH.png", "FAGU.png", "HREW.png", "MGDX.png", "PTYG.png", "RQWM.png", "VBLC.png", "XSMX.png",
        "ARRQ.png", "FCGP.png", "HVLT.png", "MPMJ.png", "PVDH.png", "SAKQ.png", "VCWF.png", "XYQF.png",
        "ASAB.png", "FHZT.png", "JFSU.png", "MSTJ.png", "QKHT.png", "script.py", "VFGD.png", "YBVT.png",
        "BHMK.png", "FPJS.png", "JKBZ.png", "MTQU.png", "QQSN.png", "SSRQ.png", "VGWK.png", "YFRQ.png",
        "CAKU.png", "FPXN.png", "JMJL.png", "MZBC.png", "QRGW.png", "STJP.png", "VPMX.png", "YKXR.png",
        "CBYH.png", "FWBG.png", "JSEM.png", "NBDN.png", "QUQD.png", "SUGC.png", "VQFS.png", "YUHN.png",
        "CCAL.png", "GBHB.png", "KAXM.png", "NBTC.png", "QUYW.png", "SZFZ.png", "VZJS.png", "YVAW.png",
        "DCJS.png", "GDHP.png", "KFUE.png", "NJMV.png", "QXCP.png", "TFDD.png", "WBAP.png", "YXNR.png",
        "DTUP.png", "GMGJ.png", "KSSA.png", "NPUW.png", "QZLV.png", "TLLA.png", "XBKV.png", "ZKJW.png",
        "EAMQ.png", "GVVS.png", "KURA.png", "NXSH.png", "RAFE.png", "TYZL.png", "XCCS.png", "ZRFJ.png",
        "EEAY.png", "GYGM.png", "LJKF.png", "NZLQ.png", "RFPY.png", "UHBT.png", "XDKZ.png",
        "EPXX.png", "HMRU.png", "LLEQ.png", "PLKT.png", "RFXN.png", "UJUN.png", "XDXF.png",
        "ESXY.png", "HNWE.png", "LUCX.png", "PLNX.png", "RNME.png", "UVZQ.png", "XNZY.png"
    ]
    total_accuracy = 0.0
    total_images = len(image_files)
    ground_truth = [
        "AACH", "FAGU", "HREW", "MGDX", "PTYG", "RQWM", "VBLC", "XSMX",
        "ARRQ", "FCGP", "HVLT", "MPMJ", "PVDH", "SAKQ", "VCWF", "XYQF",
        "ASAB", "FHZT", "JFSU", "MSTJ", "QKHT", "script.py", "VFGD", "YBVT",
        "BHMK", "FPJS", "JKBZ", "MTQU", "QQSN", "SSRQ", "VGWK", "YFRQ",
        "CAKU", "FPXN", "JMJL", "MZBC", "QRGW", "STJP", "VPMX", "YKXR",
        "CBYH", "FWBG", "JSEM", "NBDN", "QUQD", "SUGC", "VQFS", "YUHN",
        "CCAL", "GBHB", "KAXM", "NBTC", "QUYW", "SZFZ", "VZJS", "YVAW",
        "DCJS", "GDHP", "KFUE", "NJMV", "QXCP", "TFDD", "WBAP", "YXNR",
        "DTUP", "GMGJ", "KSSA", "NPUW", "QZLV", "TLLA", "XBKV", "ZKJW",
        "EAMQ", "GVVS", "KURA", "NXSH", "RAFE", "TYZL", "XCCS", "ZRFJ",
        "EEAY", "GYGM", "LJKF", "NZLQ", "RFPY", "UHBT", "XDKZ",
        "EPXX", "HMRU", "LLEQ", "PLKT", "RFXN", "UJUN", "XDXF",
        "ESXY", "HNWE", "LUCX", "PLNX", "RNME", "UVZQ", "XNZY"
    ]

    for image_file, ground_truth_text in zip(image_files, ground_truth):
        image_path = os.path.join(image_file)
        
        if os.path.isfile(image_path) and image_file.lower().endswith((".png", ".jpg", ".jpeg")):
            extracted_text = extract_text(image_path)
            extracted_text = post_process_text(extracted_text)
            
            accuracy = calculate_accuracy(extracted_text, ground_truth_text)
            total_accuracy += accuracy
            print(f"Text extracted from {image_file}: {extracted_text} , and occuracy is : {accuracy:.2f}%")
        
    overall_accuracy = total_accuracy / total_images
    print(f"Overall Accuracy: {overall_accuracy:.2f}%")