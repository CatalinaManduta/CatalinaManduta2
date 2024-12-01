function plusSlides(n, slideClass){
    const slides=document.querySelectorAll(`.${slideClass}`);
    let activeIndex=Array.from(slides).findIndex(slide=>slide.classList.contains('active'));

    slides[activeIndex].classList.remove('active');
    slides[activeIndex].style.display='none';
    activeIndex+=n;

    if(activeIndex>=slides.length)activeIndex=0;
    if(activeIndex<0)activeIndex=slides.length-1;

    slides[activeIndex].classList.add('active');
    slides[activeIndex].style.display='block';
}

document.addEventListener("DOMContentLoaded",function(){
    document.querySelectorAll('.education-slide,.personal-slide').forEach(slide=>{
        slide.style.display='none';
    });
    document.querySelector('.education-slide.active').style.display='block';
    document.querySelector('.personal-slide.active').style.display='block';
});
