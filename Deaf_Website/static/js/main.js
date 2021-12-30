var words = document.querySelectorAll('.tabs-menu li a'),
    wordContainer = document.querySelectorAll('.content-main .z-content-inner'),
    photoLabel = document.querySelectorAll('.photo-label'),
    file_upload_photo = document.querySelector('.file_upload_photo'),
    file_upload_video = document.querySelector('.file_upload_video'),
    photo_file_name = document.querySelector('.photo_file_name'),
    video_file_name = document.querySelector('.video_file_name'),
    search_input = document.querySelector('.search-input');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

console.log(search_input)
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
                console.log(output)
                if(output.length){
                    for (let i = 0; i < output.length; i++) {
                        const element = output[i];
                        console.log(element)
                        dropdownMenu.insertAdjacentHTML('beforeend', `<li><button class="no-sidebar-search" name="words_search" value="${element}"><i class="fas fa-chevron-left drop-icon" aria-hidden="true"></i><span>${element}</span></button></li>`)
                    }
                }else{
                    $('.dropdownContainer').removeClass('search-input-show');
                }

            }, error: function(response){
                console.log(response)
            }
        });
    }else{
        $('.dropdownContainer').removeClass('search-input-show');
    }
});

$(document).ready(function () {
    var objID = words[0].dataset.getinfor;
    console.log(objID)
    console.log($(`#word-${objID}`))
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
                selectedWordContainer.innerHTML = contentFilter(
                    fields.pk, 
                    fields.fields,
                    videoFilter(fields.fields.video, fields.fields.thumbnail),
                    photoFilter([fields.fields.image])
                );

                photoLabel = document.querySelectorAll('.photo-label');

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

                var newSlider = $('.project-minimal-slider');
                init_carousel(newSlider, [fields.fields.image].length);
                event.removeEventListener('click', foo);
                event.removeEventListener('touchstart', foo);
            }, error: function(response){
                console.log(response)
            }
        });
    }
});

file_upload_photo.addEventListener('change', function(){
    const file = file_upload_photo.files[0]
    if(file){
        photo_file_name.innerHTML = file.name;
        $('.image_review').show();
        $('.remove_image').show();
        const image_reader = new FileReader()
        image_reader.addEventListener('load',function(){
            $('.image_review').attr('style','background-image: url(' + this.result + ');')
        });
        image_reader.readAsDataURL(file)
    }
});

$('.remove_image').on('click', function(){
    file_upload_photo.value = ''
    $('.image_review').hide();
    photo_file_name.innerHTML = 'لا يوجد ملفات'
    $('.remove_image').hide();
});

file_upload_video.addEventListener('change', function(){
    const file = file_upload_video.files[0]
    if(file){
        video_file_name.innerHTML = file.name;
        $('.remove_video').show();
    } 

});

$('.remove_video').on('click', function(){
    video_file_name.value = ''
    video_file_name.innerHTML = 'لا يوجد ملفات'
    $('.remove_video').hide();
});

