def update_labels(
    label_path, x_min_crop, y_min_crop, new_imW, new_imH, old_imW, old_imH
):
    # Cập nhật file nhãn dựa trên ảnh đã crop
    new_labels = []
    with open(label_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            obj_class, x_center, y_center, width, height = map(float, line.split())

            # Tính tọa độ gốc của bounding box (theo ảnh ban đầu)
            old_x_min = (x_center - width / 2) * old_imW
            old_y_min = (y_center - height / 2) * old_imH
            old_x_max = (x_center + width / 2) * old_imW
            old_y_max = (y_center + height / 2) * old_imH

            # Điều chỉnh bounding box theo vùng đã crop
            new_x_min = max(0, old_x_min - x_min_crop)
            new_y_min = max(0, old_y_min - y_min_crop)
            new_x_max = min(new_imW, old_x_max - x_min_crop)
            new_y_max = min(new_imH, old_y_max - y_min_crop)

            # Bỏ qua các đối tượng không nằm trong vùng crop
            if new_x_min < new_x_max and new_y_min < new_y_max:
                new_x_center = (new_x_min + new_x_max) / 2 / new_imW
                new_y_center = (new_y_min + new_y_max) / 2 / new_imH
                new_width = (new_x_max - new_x_min) / new_imW
                new_height = (new_y_max - new_y_min) / new_imH

                # Kiểm tra nếu tọa độ trung tâm nằm trong vùng hợp lệ
                if 0 <= new_x_center <= 1 and 0 <= new_y_center <= 1:
                    new_labels.append(
                        f"{int(obj_class)} {new_x_center:0.6f} {new_y_center:0.6f} {new_width:0.6f} {new_height:0.6f}"
                    )

    s = "\n".join(new_labels)
    return s
