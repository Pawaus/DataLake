import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from pixellib.instance import instance_segmentation


def object_detection_on_an_image(filestream):
    segment_image = instance_segmentation()
    segment_image.load_model("./../mask_rcnn_coco.h5")

    #target_class = segment_image.select_target_classes(person=True)

    result = segment_image.segmentImage(
        # image_path="1city.jpg",
        # image_path=
        # image_path="2cars_people.jpeg",
        # image_path="3silicon_valley.jpg",
        # show_bboxes=True,
        # segment_target_classes=target_class,
        # extract_segmented_objects=True,
        # save_extracted_objects=True,
        # output_image_name="output.jpg"
    )

    objects_count = len(result[0]["scores"])
    print(f"Найдено объектов: {objects_count}")
