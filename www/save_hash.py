import pickle
import magic_card_detector as mcg


card_detector = mcg.MagicCardDetector(output_path='.')
card_detector.read_and_adjust_reference_images('.magic_card_detector/cards/')

hlist = []
for image in card_detector.reference_images:
    
    image.original = None
    image.clahe = None
    image.adjusted = None
    hlist.append(image)

with open('alpha_reference_phash.dat', 'wb') as f:
    pickle.dump(hlist, f)