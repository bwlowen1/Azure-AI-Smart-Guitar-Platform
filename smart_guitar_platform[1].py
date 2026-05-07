
from pathlib import Path
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face import FaceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os, argparse, json

FACE_ENDPOINT = os.environ['FACE_ENDPOINT']
FACE_KEY = os.environ['FACE_KEY']
VISION_ENDPOINT = os.environ['VISION_ENDPOINT']
VISION_KEY = os.environ['VISION_KEY']

face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_KEY))
doc_client  = DocumentAnalysisClient(endpoint=VISION_ENDPOINT, credential=AzureKeyCredential(VISION_KEY))
lang_client = TextAnalyticsClient(endpoint=VISION_ENDPOINT, credential=AzureKeyCredential(VISION_KEY))

def process_image(path):
    with open(path, 'rb') as f:
        faces = face_client.face.detect_with_stream(
            image=f,
            detection_model='detection_01',
            recognition_model='recognition_01',
            return_face_id=True
        )
    boxes = [{'left': fr.face_rectangle.left,
              'top': fr.face_rectangle.top,
              'width': fr.face_rectangle.width,
              'height': fr.face_rectangle.height} for fr in faces]
    return {'file': Path(path).name, 'defect_boxes': boxes}

def process_invoice(path):
    with open(path,'rb') as f:
        poller = doc_client.begin_analyze_document('prebuilt-invoice', document=f)
        result = poller.result()
    fields = {k: v.value for k,v in result.documents[0].fields.items()}
    return {'file': Path(path).name, 'fields': fields}

def process_email(path):
    text = Path(path).read_text(encoding='utf-8')
    sent  = lang_client.analyze_sentiment([text])[0]
    kps   = lang_client.extract_key_phrases([text])[0].key_phrases
    return {'file': Path(path).name, 'sentiment': sent.sentiment,
            'confidence': sent.confidence_scores.__dict__, 'key_phrases': kps}

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample', nargs=3, metavar=('IMAGE','INVOICE','EMAIL'), required=True)
    args=parser.parse_args()

    print('\n=== Vision (Face) ===')
    print(json.dumps(process_image(args.sample[0]), indent=2))

    print('\n=== Form Recognizer (Invoice) ===')
    print(json.dumps(process_invoice(args.sample[1]), indent=2))

    print('\n=== Text Analytics (Email) ===')
    print(json.dumps(process_email(args.sample[2]), indent=2))
