
# coding: utf-8
from pycocotools.coco import COCO
import collections
import random
import skimage.io as io
import matplotlib.pyplot as plt
import json


#[0鼻、1左目、2右目、3左耳、4右耳、5左肩、6右肩、7左肘、8右肘、9左手首、10右手首、11左腰、12右腰、13左ひざ、14右膝、15左足首、16右足首]
def get_keypoints(annos):
    keypoints = [d.get('keypoints') for d in annos]
    return{ 
        'leftchest'       : keypoints[0][34],
        'rightchest'     : keypoints[0][37],
        'leftleg'            : keypoints[0][40],
        'rightleg'          : keypoints[0][43],
        'leftankle'        : keypoints[0][46],
        'rightankle'      : keypoints[0][49],
        'leftear'            : keypoints[0][10],
        'rightear'          : keypoints[0][13],
        'leftshoulder'   : keypoints[0][16],
        'rightshoulder' : keypoints[0][19]   
    }

def show_five_imgs(img_idlist, anno_idlist,coco):
    for num in range(5):
        i = random.randrange(len(anno_idlist))
        img_id = img_idlist[i]
        img_info = coco.loadImgs(img_id)
        l = io.imread(img_info[0]['coco_url'])
        plt.figure()
        plt.imshow(l)
        annos = coco.loadAnns(anno_idlist[i])
        coco.showAnns(annos)

def get_unique_num(idlist1, idlist2):     
    num_1= collections.Counter(idlist1)
    num_2= collections.Counter(idlist2)
    return num_1, num_2


#アノテーション分類

#人が写っていない画像を除く
def get_people(coco):
    cat_ids = 1
    img_id =  coco.getImgIds(catIds=cat_ids)
    anno_ids = coco.getAnnIds(img_id)
    img_ids_byannos = []
    for i in range(len(anno_ids)):
        annos = coco.loadAnns(anno_ids[i])
        img_id_byannos = annos[0]['image_id']
        img_ids_byannos.append(img_id_byannos)
    return  {
            'img_people'       : img_id,
            'anno_people'      : anno_ids,
            'img_people_byannos' :img_ids_byannos
    }

        
#keypointsの数がkよりアノテーション数が少ないものを除く
def get_enough_keypoints(k, img_idlist, anno_idlist, coco):
    img_keypoints = []
    anno_keypoints =[]
    img_lesskeypoints = []
    anno_lesskeypoints =[]
    img_onlylesskeypoints = []
    
    for i in range(len(anno_idlist)):
        anno_ids = anno_idlist[i]
        annos = coco.loadAnns(anno_ids)
        num_keypoints = annos[0]['num_keypoints']
        img_id = img_idlist[i]
        if num_keypoints >= k:
            img_keypoints.append(img_id)
            anno_keypoints.append(anno_ids)
        else:
            img_lesskeypoints.append(img_id)
            anno_lesskeypoints.append(anno_ids)
            
    for i in range(len(img_idlist)):
        if img_idlist[i] not in img_keypoints:
            img_onlylesskeypoints.append(img_idlist[i])
            
    return{ 
        'img_keypoints'               : img_keypoints,
        'anno_keypoints'              : anno_keypoints,
        'img_lesskeypoints'           : img_lesskeypoints,
        'anno_lesskeypoints'         : anno_lesskeypoints,
        'img_onlylesskeypoints'    :img_onlylesskeypoints
    }


#両手首見えないor両足首が見えないものを除く
def get_wrist_ankle(img_idlist, anno_idlist, coco):
    img = []
    anno= []
    img_nonpart=[]
    anno_nonpart=[]
    
    for i in range(len(anno_idlist)):
        img_id = img_idlist[i]
        anno_ids = anno_idlist[i]
        annos = coco.loadAnns(anno_idlist[i])
        keypoints = [d.get('keypoints') for d in annos]

        if (keypoints[0][29] != 2 and keypoints[0][32] != 2) or (keypoints[0][47] != 2 and keypoints[0][50] != 2):
            img_nonpart.append(img_id)
            anno_nonpart.append(anno_ids)
        else:
            img.append(img_id)
            anno.append(anno_ids)
    
    return{
        'img_showpart'       : img,
        'anno_showpart'     : anno,
        'img_nonpart'          : img_nonpart,
        'anno_nonpart'        : anno_nonpart
    }

#片足でも膝が腰より高いもの or 両膝が見えないものを除く
def get_lowlegs(img_idlist, anno_idlist, coco):
    img_lowlegs = []
    anno_lowlegs = []
    img_highlegs =[]
    anno_highlegs = []

    for i in range(len(anno_idlist)):
        img_id = img_idlist[i]
        anno_ids = anno_idlist[i]
        annos = coco.loadAnns(anno_idlist[i])
        pose = get_keypoints(annos)
        
#膝が見えない　and 腰が見えないもの は 各 keypointsが0となり、条件を満たさない
#膝が見えない　and 腰が見えるものは　膝のkeypoint=0 < 腰のkeypointとなり条件を満たさない
#膝が見える　and 腰が見えないものは　膝のkeypoints > 腰のkeypoint=0となり条件を満たす
        if pose['leftleg'] > pose['leftchest'] and pose['leftleg'] > pose['rightchest'] and pose['rightleg'] > pose['leftchest'] and pose['rightleg']> pose['rightchest']:
                img_lowlegs.append(img_id)
                anno_lowlegs.append(anno_ids)
        else:
            img_highlegs.append(img_id)
            anno_highlegs.append(anno_ids)
            
    return{
        'img_lowlegs'    : img_lowlegs,
        'anno_lowlegs'  : anno_lowlegs,
        'img_highlegs'   : img_highlegs,
        'anno_highlegs' : anno_highlegs
    }

def remove_sitting(ratio, shoulder, pose):   
    #右腰基準
    if (pose['rightchest']-shoulder)/(pose['leftankle']-pose['rightchest']+0.01) > ratio and (pose['rightchest']-shoulder)/(pose['rightankle']-pose['rightchest']+0.01)> ratio:
                return True
    #左腰基準
    if (pose['leftchest']-shoulder)/(pose['leftankle']-pose['leftchest']+0.01) > ratio and         (pose['leftchest']-shoulder)/(pose['rightankle']-pose['leftchest']+0.01)> ratio:
              return True
            
    return False

#腰掛けている人or 両肩が見えない人　or 両膝が見えていない人　を除く
# ratio : (上半身/下半身)の比率    (肩〜腰)/(腰〜足首)
#ratioより値が小さいものが座っているデータ
def get_standing(ratio, img_idlist, anno_idlist, coco):   
    img_standing = []
    anno_standing = []
    img_sitting =[]
    anno_sitting = []
    
    for i in range(len(anno_idlist)):
        img_id = img_idlist[i]
        anno_ids = anno_idlist[i]
        annos = coco.loadAnns(anno_idlist[i])
        pose = get_keypoints(annos)
        chest = [pose['leftchest'], ['rightchest']]
    #右肩が写っているとき
        if pose['rightshoulder'] != 0 :
            if remove_sitting(ratio, pose['rightshoulder'], pose):
                img_sitting.append(img_id)
                anno_sitting.append(anno_ids)

    #左肩が写っている時
        elif pose['leftshoulder'] != 0 and remove_sitting(ratio, pose['leftshoulder'], pose):
            img_sitting.append(img_id)
            anno_sitting.append(anno_ids)

        if anno_ids not in anno_sitting:
            img_standing.append(img_id)
            anno_standing.append(anno_ids)
            
    return{
        'img_standing'   : img_standing,
        'anno_standing' : anno_standing,
        'img_sitting'       : img_sitting,
        'anno_sitting'     : anno_sitting
    }

#classifyしたデータのjsonファイル作成
def make_classifiedjson(json_original, json_new, img_idlist, anno_idlist ,coco):
    #オリジナルのjsonファイルからinfo, licenses, categoriesの情報を取得
    with open(json_original,"r") as f:
        original_data = json.load(f)
    info = original_data["info"]
    licenses = original_data['licenses']
    categories = original_data['categories']

    #IDリストからimage informationやannotationを取得
    img_info = coco.loadImgs(img_idlist)
    annos = coco.loadAnns(anno_idlist)

    #jsonファイルに書き込み
    new_data = {"info": info, "licenses": licenses , "imgaes": img_info, "annotations" : annos, "categories": categories}
    new_data2 = json.dumps(new_data)
    with open(json_new, "w") as f:
        f.write(new_data2)


