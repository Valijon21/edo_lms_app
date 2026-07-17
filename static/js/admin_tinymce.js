function initTinyMCE(selector) {
    tinymce.init({
        selector: selector,
        height: 500,
        plugins: 'lists link image code table media wordcount lists',
        toolbar: 'undo redo | styles | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | code',
        menubar: true,
        branding: false,
        image_title: true,
        automatic_uploads: true,
        file_picker_types: 'image',
        images_upload_handler: function (blobInfo, progress) {
            return new Promise(function (resolve, reject) {
                var xhr = new XMLHttpRequest();
                xhr.withCredentials = false;
                xhr.open('POST', '/admin/upload-image/');

                // Get CSRF Token from cookie
                var getCookie = function (name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = cookies[i].trim();
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                };

                var csrftoken = getCookie('csrftoken');
                if (csrftoken) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }

                xhr.upload.onprogress = function (e) {
                    progress(e.loaded / e.total * 100);
                };

                xhr.onload = function () {
                    if (xhr.status === 403) {
                        reject({ message: 'CSRF Token xatosi yoki Ruxsat etilmagan', remove: true });
                        return;
                    }
                    if (xhr.status < 200 || xhr.status >= 300) {
                        reject('Server xatosi: ' + xhr.status);
                        return;
                    }

                    try {
                        var json = JSON.parse(xhr.responseText);
                        if (!json || typeof json.location !== 'string') {
                            reject('Noto\'g\'ri server javobi: ' + xhr.responseText);
                            return;
                        }
                        resolve(json.location);
                    } catch (err) {
                        reject('Javobni o\'qib bo\'lmadi: ' + xhr.responseText);
                    }
                };

                xhr.onerror = function () {
                    reject('Rasm yuklashda tarmoq xatosi yuz berdi.');
                };

                var formData = new FormData();
                formData.append('file', blobInfo.blob(), blobInfo.filename());

                xhr.send(formData);
            });
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    // 1. Dars sahifasida mavjud bo'lgan textarealar uchun TinyMCE ni ishga tushirish
    initTinyMCE('textarea[name="content"], textarea[name$="-content"]');

    // 2. Django Admin inline formset (yangi dars qo'shilganda) dinamik ravishda TinyMCE ni ulash
    var $ = window.jQuery || (window.django && window.django.jQuery);
    if ($) {
        $(document).on('formset:added', function (event, $row, formsetName) {
            $row.find('textarea[name$="-content"]').each(function () {
                var id = $(this).attr('id');
                if (id) {
                    // Agar allaqachon tinymce ishga tushgan bo'lsa uni avval tozalaymiz
                    tinymce.remove('#' + id);
                    initTinyMCE('#' + id);
                }
            });
        });
    }
});
