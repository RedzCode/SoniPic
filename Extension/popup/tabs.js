const slider = document.querySelector('.slider');
const prevButton = document.getElementById('sd-left');
const nextButton = document.getElementById('sd-right');

nextButton.onclick = function () {
    var container = document.getElementById('slider');
    sideScroll(container,'right',25,43,10);
};

prevButton.onclick = function () {
    var container = document.getElementById('slider');
    sideScroll(container,'left',25,43,10);
};

function sideScroll(element,direction,speed,distance,step){
    scrollAmount = 0;
    var slideTimer = setInterval(function(){
        if(direction == 'left'){
            element.scrollLeft -= step;
        } else {
            element.scrollLeft += step;
        }
        scrollAmount += step;
        if(scrollAmount >= distance){
            window.clearInterval(slideTimer);
        }
    }, speed);
}

