<link rel="stylesheet" href="style.css">

<?php
set_time_limit(100);
$prompt = $_POST['prompt'];

$filename = __DIR__ . '/file.txt';
 
$fh = fopen($filename, 'w');
fwrite($fh, "$prompt");
fclose($fh);

$python = shell_exec('C:\Users\Home\AppData\Local\Programs\Python\Python310\python.exe text2img.py');
echo $python;

$dalle_img = "./Image/Dalle/{$prompt}.png";
$sd_img = "./Image/SD/{$prompt}.png";

if(file_exists($dalle_img) && file_exists($sd_img)) {
    echo "
    <div class='container'>
        <div class='img_container'>
            <h2>DALLE Image</h2>
            <img src='{$dalle_img}' alt='Dalle' class='img'>
        </div>
        <div class='img_container'>
            <h2>Stable Difusion Image</h2>
            <img src='{$sd_img}' alt='SD' class='img'>
        </div>
    </div>
    ";
} else {
    echo "Ошибка";
}
