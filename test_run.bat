@echo off

rem Tạo nội dung JSON trong file tạm options.json
echo {"cover_yolo_string": "", "cover_yolo_string__resize_after_crop_WH": [800, 600], "Random_varian_delta_in_percent": 10, "Brightness": 30, "Shadow_Brightness": 0, "Contrast": 1.2, "Saturation": 0, "Hue": 0} > options.json

for /L %%i in (1,1,5) do (
     ntanh_aug 20 %%i options.json D:\Dir_input D:\Dir_Output
)

rem Xóa file tạm sau khi hoàn tất
del options.json
