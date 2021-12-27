var words = document.querySelectorAll('.tabs-menu li a'),
    wordContainer = document.querySelectorAll('.content-main .z-content-inner'),
    photoLabel = document.querySelectorAll('.photo-label');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
        dots: false,
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
        event.removeEventListener('click', foo);
        event.removeEventListener('touchstart', foo);
        
        var selectedWordContainer = wordContainer.item(index);
        var  objID = event.dataset.getinfor;

        console.log(event)

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
                    videoFilter(fields.fields.video),
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
            }
        });
    }
});