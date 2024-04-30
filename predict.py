import os
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np

images_dir = os.path.join('.', 'test', 'images')
model_path = os.path.join('.', 'runs', 'detect', 'train2', 'weights', 'best.pt')
# Load a model
model = YOLO('weights/best.pt')


def digit_detection(image_path):
    img = cv2.imread(image_path)
    results = model.predict(img)[0]
    threshold = 0.5
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    result_detections = []
    for result in results.boxes.data.tolist():
        print(result)
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(img, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            result_detections.append((class_id, x1, y1, x2, y2))

    image_path_out = '{}_out.jpg'.format(image_path)
    cv2.imwrite(image_path_out, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Создаем список координат объектов
    detections_coord = []
    for detect in result_detections:
        detections_coord.append((detect[0], detect[1], detect[2], detect[3],
                                 detect[4], abs(detect[2] - detect[4])))

    detections_array = np.array(detections_coord)
    same_level_min_objects = []
    same_level_max_objects = []
    # 0 - flag current max, 1 - current min
    if detections_array.shape[0] >= 2:
        if ((detections_array[0, 5] > 2 * detections_array[1, 5]) and
                (abs(detections_array[0, 5] - detections_array[1, 5]) > 10.0)):
            same_level_max_objects.append(detections_coord[0])
            same_level_min_objects.append(detections_coord[1])
            flag = 1
        elif ((detections_array[0, 5] < 2 * detections_array[1, 5]) and
                (abs(detections_array[0, 5] - detections_array[1, 5]) > 10.0)):
            same_level_min_objects.append(detections_coord[0])
            same_level_max_objects.append(detections_coord[1])
            flag = 0
        elif ((detections_array[0, 5] < 2 * detections_array[1, 5]) and
                (detections_array[1, 5]) < 60):
            same_level_min_objects.append(detections_coord[0])
            same_level_min_objects.append(detections_coord[1])
            flag = 1
        else:
            same_level_max_objects.append(detections_coord[0])
            same_level_max_objects.append(detections_coord[1])
            flag = 0

        if len(same_level_max_objects) == 2:
            obj1, obj2 = same_level_max_objects
            obj1_center_x = (obj1[1] + obj1[3]) / 2
            obj2_center_x = (obj2[1] + obj2[3]) / 2

            if obj1_center_x < obj2_center_x:
                return obj1[0] + (obj2[0]) / 10
            elif obj1_center_x > obj2_center_x:
                return obj2[0] + (obj1[0]) / 10
            else:
                return obj1[0] + (obj2[0]) / 10

        current_height = detections_array[1, 5]

        if detections_array.shape[0] > 2:
            same_level_max_objects_copy = same_level_max_objects
            same_level_min_objects_copy = same_level_min_objects
            for i in range(2, len(detections_array)):
                if detections_array[i, 5] > 2 * current_height and flag == 1:
                    same_level_max_objects_copy.append(detections_coord[i])
                    current_height = detections_array[i, 5]
                elif detections_array[i, 5] < 2 * current_height and flag == 0:
                    same_level_min_objects_copy.append(detections_coord[i])
                    current_height = detections_array[i, 5]
                elif detections_array[i, 5] < 2 * current_height and flag == 1:
                    same_level_min_objects_copy.append(detections_coord[i])
                    current_height = detections_array[i, 5]
                elif detections_array[i, 5] < 2 * current_height and flag == 0:
                    same_level_max_objects_copy.append(detections_coord[i])
                    current_height = detections_array[i, 5]

            if len(same_level_max_objects_copy) == 3:
                obj1, obj2, obj3 = same_level_max_objects_copy

                # Определяем положение объектов
                obj1_obj2_position = get_object_position(obj1[1], obj1[2], obj1[3], obj1[4],
                                                         obj2[1], obj2[2], obj2[3], obj2[4])
                obj1_obj3_position = get_object_position(obj1[1], obj1[2], obj1[3], obj1[4],
                                                         obj3[1], obj3[2], obj3[3], obj3[4])
                obj2_obj3_position = get_object_position(obj2[1], obj2[2], obj2[3], obj2[4],
                                                         obj3[1], obj3[2], obj3[3], obj3[4])

                # Определяем позиции объектов на основе их относительного положения
                if (obj1_obj2_position == 'Первый объект слева от второго' and
                        obj1_obj3_position == 'Первый объект слева от второго'):
                    return (obj1[0] * 10) + (obj2[0]) + (obj3[0]) / 10
                elif (obj1_obj2_position == 'Первый объект слева от второго' and
                        obj2_obj3_position == 'Первый объект слева от второго'):
                    return (obj1[0] * 10) + (obj3[0]) + (obj2[0]) / 10
                elif (obj1_obj3_position == 'Первый объект слева от второго' and
                        obj2_obj3_position == 'Первый объект слева от второго'):
                    return obj2[0] * 10 + (obj1[0]) + (obj3[0]) / 10

    if detections_array.shape[0] < 2:
        return 'Пожалуйста повторите снимок'


def get_object_position(x1, y1, x2, y2, x3, y3, x4, y4):
    # Координаты первого объекта
    obj1_x1, obj1_y1, obj1_x2, obj1_y2 = x1, y1, x2, y2

    # Координаты второго объекта
    obj2_x1, obj2_y1, obj2_x2, obj2_y2 = x3, y3, x4, y4

    # Определяем центры объектов
    obj1_center_x = (obj1_x1 + obj1_x2) / 2
    obj2_center_x = (obj2_x1 + obj2_x2) / 2

    # Определяем относительное положение объектов
    if obj1_center_x < obj2_center_x:
        return 'Первый объект слева от второго'
    elif obj1_center_x > obj2_center_x:
        return 'Первый объект справа от второго'
