$(document).ready(function() {

    var select = $('select[multiple]');
    var options = select.find('option');

    var div = $('<div />').addClass('selectMultiple');
    var active = $('<div />');
    var list = $('<ul />');
    var placeholder = select.data('placeholder');

    var span = $('<span />').text(placeholder).appendTo(active);

    options.each(function() {
        var text = $(this).text();
        if($(this).is(':selected')) {
            active.append($('<a />').html('<em>' + text + '</em><i></i>'));
            span.addClass('hide');
        } else {
            list.append($('<li />').html(text));
        }
    });

    active.append($('<div />').addClass('arrow').html('<i class="fas fa-caret-down"></i>'));
    div.append(active).append(list);

    select.wrap(div);

    $(document).on('click', '.selectMultiple ul li', function(e) {
        var select = $(this).parent().parent();
        var li = $(this);
        if(!select.hasClass('clicked')) {
            select.addClass('clicked');
            li.prev().addClass('beforeRemove');
            li.next().addClass('afterRemove');
            li.addClass('remove');
            var a = $('<a />').addClass('notShown').html('<em>' + li.text() + '</em><i></i>').hide().appendTo(select.children('div'));
            a.slideDown(400, function() {
                setTimeout(function() {
                    a.addClass('shown');
                    select.children('div').children('span').addClass('hide');
                    select.find('option:contains(' + li.text() + ')').prop('selected', true);
                }, 500);
            });
            setTimeout(function() {
                if(li.prev().is(':last-child')) {
                    li.prev().removeClass('beforeRemove');
                }
                if(li.next().is(':first-child')) {
                    li.next().removeClass('afterRemove');
                }
                setTimeout(function() {
                    li.prev().removeClass('beforeRemove');
                    li.next().removeClass('afterRemove');
                }, 200);

                li.slideUp(400, function() {
                    li.remove();
                    select.removeClass('clicked');
                });
            }, 600);
        }
    });

    $(document).on('click', '.selectMultiple > div a', function(e) {
        var select = $(this).parent().parent();
        var self = $(this);
        self.removeClass().addClass('remove');
        select.addClass('open');
        setTimeout(function() {
            self.addClass('disappear');
            setTimeout(function() {
                self.animate({
                    width: 0,
                    height: 0,
                    padding: 0,
                    margin: 0
                }, 300, function() {
                    var li = $('<li />').text(self.children('em').text()).addClass('notShown').appendTo(select.find('ul'));
                    li.slideDown(400, function() {
                        li.addClass('show');
                        setTimeout(function() {
                            select.find('option:contains(' + self.children('em').text() + ')').prop('selected', false);
                            if(!select.find('option:selected').length) {
                                select.children('div').children('span').removeClass('hide');
                            }
                            li.removeClass();
                        }, 400);
                    });
                    self.remove();
                })
            }, 300);
        }, 400);
    });

    $(document).on('click', '.selectMultiple > div .arrow, .selectMultiple > div span', function(e) {
        $(this).parent().parent().toggleClass('open');
    });

});

var vote_open = document.querySelectorAll('.gmg-sp-header'),
    vote_close = document.querySelectorAll('.gmg-sp-close'),
    opinion_form = document.querySelectorAll('#opinion-form');


opinion_form.forEach(function(event){
    event.addEventListener('submit', function(e){
        e.preventDefault();
        const csrftoken = event.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            url: "/user_word_vote/",
            data: {'word':event.dataset.word,
            'vote':e.submitter.name
            },
            beforeSend: function(){
                event.innerHTML = `<div class="opinion-form-text"> <span> جاري إرسال رأيك  <strong>...</strong></span></div>`;
            },
            success: function (response) {
                console.log(response)
                if(response == 'agree'){
                    event.innerHTML = `<div class="opinion-form-text"> <span> لقد <strong>وافقت</strong> على هذا المنشور، شكرا لإبداء رأيك.</span></div>`;
                }else if(response == 'disagree'){
                    event.innerHTML = `
                        <div class="opinion-form-text">
                            <span> لقد <strong>اعترضت</strong> على هذا المنشور، شكرا لإبداء رأيك.</span>
                            <span data-target="#m-a-f-${event.dataset.word}" data-toggle="modal" class="modal-button" style="text-decoration: underline;font-size:13px;opacity:0.65"><strong>اقترح</strong> منشور اخر اللآن</span>
                        </div>
                    `
                }
            }
        });
    })
})

vote_open.forEach(function(event){
    event.addEventListener('click',function(){
        console.log(event)
        $(event.parentElement).toggleClass( 'open' );
    });
})

vote_close.forEach(function(event){
    event.addEventListener('click',function(){
        console.log(event)
        // $('#gmg-side-popup').toggleClass( 'open' );
    });
})
