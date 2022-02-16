var words = document.querySelectorAll('.tabs-menu li a'),
    wordContainer = document.querySelectorAll('.content-main .z-content-inner'),
    photoLabel = document.querySelectorAll('.photo-label'),
    photo_input_content = document.querySelectorAll('.photo-input-content'),
    remove_image = document.querySelectorAll('.file_topic_upload .remove_image'),
    video_input_content = document.querySelectorAll('.video-input-content'),
    remove_video = document.querySelectorAll('.file_topic_upload .remove_video'),
    search_input = document.querySelector('.search-input'),
    modal = document.querySelectorAll('.modal-footer button');

var vids = $(".video-thumb"); 

vids.each(vids, function(){
    this.controls = false; 
}); 

photo_input_content.forEach(function(photo){
    photo.addEventListener('change', function(e){
        var file_upload_photo = this.querySelector('.file_upload_photo'),
        photo_file_name = this.querySelector('.photo_file_name'),
        remove_image = this.querySelector('.remove_image'),
        image_review = this.parentElement.querySelector('.image_review'),
        btn_file_upload = this.querySelector('.post_file_upload');

        const file = file_upload_photo.files[0]
        if(file){
            photo_file_name.innerHTML = file.name;
            btn_file_upload.innerHTML = 'اضافة صورة للمحتوى';
            if(file.type.includes('image')){
                const image_reader = new FileReader()
                image_reader.addEventListener('load',function(){
                    $(image_review).attr('style','background-image: url(' + image_reader.result + ');')
                    $(image_review).show();
                });
                image_reader.readAsDataURL(file)
            }else{
                $(image_review).hide();
            }

            $(remove_image).show();
        }
    });
});

remove_image.forEach(function(image){
    image.addEventListener('click', function(){
        var parent_image = image.parentElement.parentElement,
            file_upload_photo = parent_image.querySelector('.file_upload_photo'),
            photo_file_name = parent_image.querySelector('.photo_file_name'),
            image_review = parent_image.querySelector('.image_review'),
            check_list = parent_image.querySelector('.check-list-image'),
            file_upload_video = parent_image.parentElement.querySelector('.file_upload_video');

        file_upload_photo.value = ''
        $(image_review).hide();
        photo_file_name.innerHTML = 'لا يوجد ملفات'
        $(image).hide();
        check_list.innerHTML = '';
    });
});

video_input_content.forEach(function(video){   
    video.addEventListener('change', function(){
        var file_upload_video = video.querySelector('.file_upload_video'),
            video_file_name = video.querySelector('.video_file_name');
            remove_video = video.querySelector('.remove_video'),
            btn_file_upload = video.querySelector('.post_file_upload');

        const file = file_upload_video.files[0]
        if(file){
            video_file_name.innerHTML = file.name;
            btn_file_upload.innerHTML = 'اضافة فيديو للمحتوى';
            $(remove_video).show();
        } 
    });
});

remove_video.forEach(function(video){
    video.addEventListener('click', function(){
        var parent_video = video.parentElement.parentElement,
            file_upload_video = parent_video.querySelector('.file_upload_video'),
            video_file_name = parent_video.querySelector('.video_file_name'),
            check_list = parent_video.querySelector('.check-list-video'),
            file_upload_photo = parent_video.parentElement.querySelector('.file_upload_photo');
        
        file_upload_video.value = ''
        video_file_name.innerHTML = 'لا يوجد ملفات'
        $(remove_video).hide();
        check_list.innerHTML = '';
    });
});

modal.forEach(function(event, index){
    $(document).on('submit', event, function(e){
        e.preventDefault();
        console.log(event)
        var modal_parent = event.parentElement.parentElement,
            file_upload_photo = modal_parent.querySelector('.file_upload_photo'),
            file_upload_video = modal_parent.querySelector('.file_upload_video'),
            file_image = file_upload_photo.files[0],
            file_video = file_upload_video.files[0];
        
        const csrftoken = modal_parent.parentElement.querySelector('[name=csrfmiddlewaretoken]').value;

        if(file_image || file_video){
            const data_dict = {'image':0, 'video':0};
            if(file_image){
                data_dict.image = {'size':file_image.size, 'ext':file_image.type};
            }
            if(file_video){
                data_dict.video = {'size':file_video.size, 'ext':file_video.type};
            }
            $.ajax({
                type: "POST",
                url: "/words_users/",
                headers: {'X-CSRFToken': csrftoken},
                data: {'input':JSON.stringify(data_dict)},
                beforeSend: function(){
                    event.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" style="margin-left: 7px"></span> <span> جاري التحقق </span>`;
                    $(event).attr('disabled','disabled');
                },
                success: function (response) {
                    var data = JSON.parse(response),
                        check_size,
                        check_ext,
                        check_list_image = modal_parent.querySelector('.check-list-image'),
                        check_list_video = modal_parent.querySelector('.check-list-video');

                    if(data.image){
                        
                        check_size = (data.image.size) ? 'fa-check check-correct':'fa-exclamation-triangle check-error';
                        check_ext = (data.image.ext) ? 'fa-check check-correct':'fa-exclamation-triangle check-error';
                        check_list_image.innerHTML = `<ul>
                        <li><i class="fas ${check_size}"></i><span>حجم الملف أقل من ${data.image.conditions.size}M</span></li>
                        <li><i class="fas ${check_ext}"></i><span>الملف المرفق من ضمن ( ${data.image.conditions.ext.join(' , ').replace('.','')} )</span></li>
                        </ul>`
                    }

                    if(data.video){
                        check_size = (data.video.size) ? 'fa-check check-correct':'fa-exclamation-triangle check-error';
                        check_ext = (data.video.ext) ? 'fa-check check-correct':'fa-exclamation-triangle check-error';
                        check_list_video.innerHTML = `<ul>
                        <li><i class="fas ${check_size}"></i><span>حجم الملف أقل من ${data.video.conditions.size}M</span></li>
                        <li><i class="fas ${check_ext}"></i><span>الملف المرفق من ضمن ( ${data.video.conditions.ext.join(', ').replace('.','')} )</span></li>
                        </ul>`
                    }

                    var check_validate = (data.image && data.video) ? (data.image.size && data.image.ext) && (data.video.size && data.video.ext):(data.image.size && data.image.ext) || (data.video.size && data.video.ext);

                    if(check_validate){

                        $(file_upload_photo).attr('disabled','disabled');
                        $(file_upload_video).attr('disabled','disabled');
                        $(event).addClass('no-hover');

                        var formDataFile = new FormData();
                        
                        formDataFile.append('image', file_image);
                        formDataFile.append('video', file_video);

                        var xhr_ajax = $.ajax({
                            type: "POST",
                            url: "/words_users_uploads/",
                            headers: {'X-CSRFToken': csrftoken},
                            data: formDataFile,
                            dataType: 'json',
                            cache: false,
                            processData: false,
                            contentType: false,
                            xhr: function(){
                                var xhr = new XMLHttpRequest(),
                                    upload_delete = modal_parent.querySelector('.upload-delete');

                                $(upload_delete).show();

                                xhr.upload.addEventListener('progress', function (e) {
                                    console.log(e)
                                    if (e.lengthComputable) {
                                        var percent = Math.round((e.loaded / e.total) * 100);
                                        event.innerHTML = `<div class="uploud-bar" style="width: ${percent}%"><span>${percent}</span> %</div><span>... جاري الرفع</span>`;
                                    }
                                });

                                upload_delete.addEventListener('click', function(){
                                    console.log(upload_delete);
                                    xhr.abort();
                                    $(upload_delete).hide();
                                    $(file_upload_photo).removeAttr('disabled','disabled');
                                    $(file_upload_video).removeAttr('disabled','disabled');
                                    $(event).removeClass('no-hover');

                                    event.innerHTML = '<span>ارسال</span>'
                                });

                                return xhr;
                            },
                            success: function (response) {
                                console.log('success');
                            }
                        });
                    }else{
                        $(event).removeAttr('disabled','disabled');
                        event.innerHTML = '<span>ارسال</span>'
                    }
                }
            });
        }
    });
});

search_input.addEventListener('input', function(event){
    var dropdownMenu = document.querySelector('.dropdownMenu');
    dropdownMenu.innerHTML = '';

    if(search_input.value){
        $('.dropdownContainer').addClass('search-input-show');
        $.ajax({
            type: "GET",
            url: "/words_search_ajax/",
            data: {'input':search_input.value},
            beforeSend: function(){
                dropdownMenu.innerHTML = preloadSearchAjax;
            },
            success: function (response) {
                dropdownMenu.innerHTML = '';
                var output = JSON.parse(response);
                if(output.length){
                    for (let i = 0; i < output.length; i++) {
                        const element = output[i];
                        dropdownMenu.insertAdjacentHTML('beforeend', `<li><button class="no-sidebar-search" name="words_search" value="${element}"><i class="fas fa-chevron-left drop-icon" aria-hidden="true"></i><span>${element}</span></button></li>`)
                    }
                }else{
                    $('.dropdownContainer').removeClass('search-input-show');
                }

            }, error: function(response){
            }
        });
    }else{
        $('.dropdownContainer').removeClass('search-input-show');
    }
});

$(document).ready(function () {
    var objID = words[0].dataset.getinfor;
    $(`#word-${objID}`)[0].click();
});

photoLabel.forEach(function(event){
    event.addEventListener('click', function(){
        window.dispatchEvent(new Event('resize'));
    });
});

function init_carousel(newSlider, photo) {
    if(photo == 1){
        var itemLength = 1;
    }else{
        var itemLength = 2;
    }

    newSlider.owlCarousel({
        rtl:true,
        nav:true,
        navText: ["<i class='flaticon-back'></i>" , "<i class='flaticon-next'></i>"],
        margin:40,
        responsive:{
            0:{
                margin:0,
                items:1
            },
            768:{
                margin:25,
                items:1
            },
            1200:{
                items: itemLength
        }
        }
    });
};

words.forEach(function(event, index){
    event.addEventListener('click', foo);
    event.addEventListener('click', function(){
        var  objID = event.dataset.getinfor;
        $(`#video-${objID}`).prop('checked', true);
    });
    event.addEventListener('touchstart', foo);
    event.addEventListener('touchstart', function(){
        var  objID = event.dataset.getinfor;
        $(`#video-${objID}`).prop('checked', true);
    });

    function foo(){
        var selectedWordContainer = wordContainer.item(index),
            objID = event.dataset.getinfor;
        
        const csrftoken = event.parentElement.parentElement.parentElement.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            url: "/words_ajax/",
            data: {'id':objID},
            beforeSend: function(){
                selectedWordContainer.innerHTML = preloadAjax;
            },
            success: function (response) {
                var fields = JSON.parse(response)[0];              

                photoLabel = document.querySelectorAll('.photo-label');

                var newSlider = $('.project-minimal-slider');
                init_carousel(newSlider, [fields.fields.image].length);
                event.removeEventListener('click', foo);
                event.removeEventListener('touchstart', foo);

                selectedWordContainer.innerHTML = contentFilter(
                    fields.pk, 
                    fields.fields,
                    videoFilter(fields.fields.video),
                    photoFilter([fields.fields.image])
                )

                photoLabel.forEach(function(event){
                    event.addEventListener('click', function(){
                        window.dispatchEvent(new Event('resize'));
                    });
                });

                photoLabel.forEach(function(event){
                    event.addEventListener('touchstart', function(){
                        window.dispatchEvent(new Event('resize'));
                    });
                });

            }, error: function(response){
            }
        });
    }
});


// function MakeVideoElement(videoURL) {
//     var video = document.createElement('video');
//     video.controls = true;
//     video.controlslist = 'nodownload';
//     video.src = videoURL;
//     return video
// }

// function generateThumbnail(selectedWordContainer, containerDone, video) {
//     var canvas = document.createElement("canvas");

//     canvas.width = 300;
//     canvas.height = 300;

//     video.addEventListener('loadeddata', function() {
//         reloadRandomFrame();
//     }, false);

//     video.addEventListener('seeked', function() {
//         var context = canvas.getContext('2d');
//         context.drawImage(video, 0, 0, canvas.width, canvas.height);
//         var pngUrl = canvas.toDataURL();
//         selectedWordContainer.innerHTML = containerDone;
//         var img = selectedWordContainer.querySelector('.our-blog .our-img');
//         img.style.background = `url('${pngUrl}') center no-repeat`;
//         img.style.backgroundSize = "cover";
//     }, false);

//     function reloadRandomFrame() {
//         if (!isNaN(video.duration)) {
//             var rand = Math.round(Math.random() * video.duration * 1000) + 1;
//             video.currentTime = rand / 1000;
//         }
//     }
// }