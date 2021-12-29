var preloadAjax = `
<div class="ctn-preloader" style="position:relative !important; background:none; min-height: 200px">
<div class="animation-preloader">
    <div class="spinner" style="width: 120px;height:120px; margin-bottom:10px"></div>
    <div class="txt-loading">
        <span data-text-preloader="جاري التحميل" class="letters-loading letters-loading-small" style="font-size: 20px; line-height:unset">
        </span>
    </div>
</div>	
</div>
`;

var preloadSearchAjax = `
<div class="ctn-preloader" style="position:relative !important; background:none; min-height: 150px">
<div class="animation-preloader">
    <div class="spinner" style="width: 60px;height:60px;margin: auto;"></div>
</div>	
</div>
`;


function videoFilter(video, thumbnail){
    console.log(video)
    if(video){
        var videoDone = `
        <div class="our-blog">
            <div class="single-blog-post">
                <div class="img-holder">
                    <img src="/uploads/${thumbnail}" alt="">
                    <a data-fancybox href="/uploads/${video}" class="fancybox video-button"><i class="flaticon-play-button-2"></i></a>
                </div>
            </div>
        </div>
        `;
    }else{
        var videoDone = `
        <div class="notFound">
            <i class="fas fa-exclamation-triangle"></i>
            <h3 class="flex">لا يوجد فيديو لعرضه</h3>
        </div>
        `
    };

    return videoDone;
};

function photoFilter(photo){
    if(photo[0]){
        var photoDone = [];
        for (let i = 0; i < photo.length; i++) {
            const element = photo[i];
            var photoLoop = `
            <div class="item">
                <div class="project-item">
                    <div class="img-box">
                    <div class="img-box-url" style="background-image: url('/uploads/${element}');"></div>
                    </div>
                    <div class="hover-valina">
                        <div>
                            <a href="/uploads/${element}" class="zoom fancybox" data-fancybox="gallery"><img src="/static/images/icon/zoom-in.svg" alt="" class="svg"></a>
                        </div>
                    </div>
                    <!-- /.hover-valina -->
                </div>
                <!-- /.project-item -->
            </div>
            `;

            photoDone.push(photoLoop);
        }
        var photoItems = photoDone.join(' ');
        photoDone = `
        <div class="element-section">
            <div class="our-project project-minimal-style">
                <div class="inner-wrapper">
                    <div class="project-minimal-slider">
                    ${photoItems}
                    </div>
                    <!-- /.inner-wrapper -->
                </div>
                <!-- /.our-project -->
            </div>
        </div>
        `;
    }else{
        var photoDone = `
        <div class="notFound">
            <i class="fas fa-exclamation-triangle"></i>
            <h3 class="flex">لا يوجد صور لعرضها</h3>
        </div>
        `;
    };

    return photoDone;
};


function contentFilter(pk, fields, video, photo){
    var textnone = `
    <input type="radio" id="video-${pk}" name="tab-control" checked>
    <input type="radio" id="photo-${pk}" name="tab-control">
    
    <ul>
            <li title="Video"><label class="video-label" for="video-${pk}" role="button"><br><span>Video</span></label></li>
            <li title="Photo"><label class="photo-label" for="photo-${pk}" role="button"><br><span>Photo</span></label></li>
    </ul>
    
    <div class="slider"><div class="indicator"></div></div>
    <div class="content">
        <section>
            <h2>Video</h2>
            ${video}
        </section>
        <section>
            <h2>Photo</h2>
            ${photo}
        </section>
    </div>
    `

    return textnone;
}

