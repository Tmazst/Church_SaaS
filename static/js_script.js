//
//// Function to handle the scroll event
//function handleScroll() {
//
////      console.log("Scroll Called1");
//      // Get the navigation menu element
//
//      // Store the last known scroll position
//      let lastScrollTop = 0;
//
//      // Get the height of the window
//      const windowHeight = window.innerHeight;
//
//      // Get the current scroll position
//      const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
//
//      // Determine the scroll direction
//      const scrollDirection = currentScroll > lastScrollTop ? 'down' : 'up';
//
//
//       if (window.innerWidth <= 768){
//          // If the user is scrolling down and the navigation is not already at the bottom
//          if (scrollDirection === 'down' && (windowHeight + currentScroll) >= document.body.offsetHeight-4000) {
//            console.log("Scroll Called",currentScroll,scrollDirection);
//          } else {
//            //write code
//          }
//          // Update the known scroll position
//          lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
//
//    }else{
//
//          var scrollingElement = document.getElementById("section-last");
//          // Distance from the top of the document to the top of the scrolling element
//          var elementOffset = scrollingElement.offsetTop;
//          // Viewport (window) top position
//          var windowTop = window.pageYOffset || document.documentElement.scrollTop;
//
//          if (windowTop > elementOffset) {
////              scrollingElement.style.position = "fixed";
////              scrollingElement.style.top = "0";
//              } else {
////                scrollingElement.style.position = "relative";
//              }
//
//    }
//}
//window.onscroll = function() {handleScroll()};

// var navOne = document.querySelector("#nav-1");
// var navOneChild = document.querySelector("#nav-chld-1");

// navOne.addEventListener("mouseenter", function(){
//     navOneChild.classList.add('reveal');

//     navOneChild.addEventListener("mouseenter", function(){
//         navOneChild.classList.add('reveal');
//         console.log(navOneChild.id);
//     })

//     navOneChild.addEventListener("mouseleave", function(){
//         navOneChild.classList.remove('reveal');
//     })

// });

// navOne.addEventListener("mouseleave", function(){
//     navOneChild.classList.remove('reveal');
// });


var navParent = document.querySelectorAll(".saas-nav-item");
navParent.forEach(nav => {
    nav.addEventListener('click', function(){
        console.log("Nav item clicked");

        // First, hide all child elements
        navParent.forEach(item => {
            var childNav = document.querySelector("#nav-chld-" + item.id.split('-')[1]);
            if (childNav) {
                childNav.classList.remove('reveal');
            }
        });

        // Show the specific child nav for the clicked item
        if (nav.id === "nav-1"){
            var navOneChild = document.querySelector("#nav-chld-1");
            navOneChild.classList.toggle('reveal'); // Use toggle to show/hide
        }else if(nav.id === "nav-2"){
            var navOneChild = document.querySelector("#nav-chld-2");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-3"){
            var navOneChild = document.querySelector("#nav-chld-3");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-4"){
            var navOneChild = document.querySelector("#nav-chld-4");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-5"){
            var navOneChild = document.querySelector("#nav-chld-5");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-6"){
            var navOneChild = document.querySelector("#nav-chld-6");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-7"){
            var navOneChild = document.querySelector("#nav-chld-7");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-8"){
            var navOneChild = document.querySelector("#nav-chld-8");
            navOneChild.classList.toggle('reveal');
        }
    });
});


// var navOneChild = document.querySelector("#nav-chld-1");

// navOne.addEventListener("mouseenter", function(){
//     navOneChild.classList.add('reveal');

//     navOneChild.addEventListener("mouseenter", function(){
//         navOneChild.classList.add('reveal');
//         console.log(navOneChild.id);
//     })

//     navOneChild.addEventListener("mouseleave", function(){
//         navOneChild.classList.remove('reveal');
//     })

// });

// navOne.addEventListener("mouseleave", function(){
//     navOneChild.classList.remove('reveal');
// });



document.addEventListener('DOMContentLoaded', function () {
    
    // const specialDietBool = document.getElementById('special_diet_bool');
    // const specialDietContainer = document.getElementById('special_diet_container');
    // const accommodationBool = document.getElementById('accommodation_bool');
    // const accommodationContainer = document.getElementById('accommodation_cont');

    // specialDietBool.addEventListener('change', function () {
    //     if (specialDietBool.checked) {
    //         specialDietContainer.style.display = 'block';
    //         specialDietContainer.classList.remove('hidden')
    //     } else {
    //         specialDietContainer.style.display = 'none';
    //     }
    // });

    const specialDietRadios = document.querySelectorAll('input[name="special_diet_bool"]');
        
    specialDietRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            const specialDietContainer = document.getElementById('special_diet_container');
            if (this.value === "1") {  // Assuming "1" means Yes
                // console.log("Assuming 1 means Yes")
                specialDietContainer.style.display = 'block';
                specialDietContainer.classList.remove('hidden');
            } else {  // Assuming anything else means No
                specialDietContainer.style.display = 'none';
            }
        });
    });
});

// });


function openDetails(id,event){
    
    console.log("ID: ",id)
    let showRegDetails = document.querySelector("#reg-info-"+id);
    let showEvDetails = document.querySelector("#ev-info-"+id);

    showRegDetails.classList.toggle("show-popup");
    showEvDetails.classList.toggle("show-popup");

    if (event.target.innerHTML === "Show Details"){
            event.target.innerHTML = "Hide";
            } else {
                event.target.innerHTML = "Show Details";
        };
};


function popUp(){
    // var popScrnLogo = document.getElementById("updates");
    // popScrnLogo.classList.toggle("show-popup");
    
    let popCont = document.querySelector('.popup-cont');
    let formCont = document.querySelector("#form-cont");

    popCont.classList.toggle("show-popup");
    formCont.style.display='none';
    
};

function closePop(){
    let popCont = document.querySelector('.popup-cont');
    let formCont = document.querySelector("#form-cont");
    popCont.classList.remove("show-popup");
    formCont.style.display='flex';
}

function popupMinutes(id){
    // var popScrnLogo = document.getElementById("updates");
    // popScrnLogo.classList.toggle("show-popup");
    
    let popCont = document.querySelector('#pop_image_' + id);
    let popUp = document.querySelector('#popup_' + id);
    // let formCont = document.querySelector("#form-cont");

    popCont.classList.toggle("show-popup");
    popUp.classList.toggle("show-popup");
    // formCont.style.display='none';
    
};

function popupSermon(id){
    // var popScrnLogo = document.getElementById("updates");
    // popScrnLogo.classList.toggle("show-popup");
    
    let popCont = document.querySelector('#pop_image_' + id);
    let popUp = document.querySelector('#popup_' + id);
    // let formCont = document.querySelector("#form-cont");

    popCont.classList.toggle("show-popup");
    popUp.classList.toggle("show-popup");
    // formCont.style.display='none';
    
};


const paragraph = document.querySelectorAll('.sel-tag');

paragraph.forEach(function(pTag){
    const words = pTag.innerText.split(' ').map(word => `<span>${word}</span>`);
    pTag.innerHTML = words.join(' ');
    pTag.classList.toggle('.sel-tag');
    });
//function pop(){
//    console.log('Mouse Over');
//}

var sections = document.querySelectorAll(".profile-sections");
var currentSectionIndex = 0;
var firstSection = sections[0];
var noSections = sections.length;
var progressCont = document.querySelectorAll(".progress-cont");
var progressCount = document.querySelectorAll(".progress-no");
let indexList = [];


function changeProgressColor(){

    for (var sect=0;sect<noSections;sect++){
        // Create Divs
        var progressCountIncr = document.createElement("div");
        var progressCircle = document.createElement("div");
        var progressLineSep = document.createElement("div");

        if (indexList.includes(sect)) {
            // Skip creating the progress element since it exists
            continue;
        }

        // Do not start from zero
        progressCountIncr.innerText = (sect+1);
        //  console.log("Current Index Outside:" + currentSectionIndex);
        //  console.log("Current Sect: Outside" + sect);
        //  Make current progress count coral in color

        if(currentSectionIndex == sect){
            // Assign Classes to divs
            progressCountIncr.classList.add("progress-no-c");
            progressCircle.classList.add("progress-incr-c");
            progressLineSep.classList.add("progress-line-sep-c");

            // Append to parents div
            progressCircle.appendChild(progressCountIncr);
            progressCont[currentSectionIndex].appendChild(progressLineSep);
            progressCont[currentSectionIndex].appendChild(progressCircle);

        }else{

//            console.log("Current Index Else:" + currentSectionIndex);
//            if (!indexList.includes(currentSectionIndex)){

                //Assign Classes to divs
                progressCircle.classList.add("progress-incr");
                progressLineSep.classList.add("progress-line-sep");
                progressCountIncr.classList.add("progress-no");

                console.log("List Indexes: ",indexList);
                }

                // Append to parents div
                progressCircle.appendChild(progressCountIncr);
                progressCont[currentSectionIndex].appendChild(progressLineSep);
                progressCont[currentSectionIndex].appendChild(progressCircle);

                indexList.push(sect);

        }

    };


const popup = document.querySelector('.pop-up');
var quoteBtns = document.querySelectorAll('.item');
var popCont = document.querySelectorAll('.pop-cont');


quoteBtns.forEach(function(btn){
    btn.addEventListener('click', function(event){
//    console.log("Contains Poster Quote: ",event.target);
     if(event.target.id === 'logo_quote_btn'){
        var popScrnLogo = document.getElementById("logo_quote");
        popScrnLogo.classList.toggle("show-popup");
        popup.classList.toggle("show-popup");

        }else if(event.target.id === 'poster_quote_btn'){
            var popScrnPoster = document.getElementById("poster_quote");
//            console.log("Contains Poster Quote: ")
            popScrnPoster.classList.toggle("show-popup");
            popup.classList.toggle("show-popup");
        }else if(event.target.id === 'flyer_quote_btn'){
            var popScrnPoster = document.getElementById("flyer_quote");
            console.log("Contains Poster Quote: ")
            popScrnPoster.classList.toggle("show-popup");
            popup.classList.toggle("show-popup");
            }
     })
});

function openMenuFunc(){
    console.log("Test2");
}

//#Menu
//const navSlide = () => {
const burger = document.querySelector(".menu-icon");
const otherNav = document.querySelector(".other-nav");
const navlinks = document.querySelectorAll(".nav-link");
//const navLinks = document.querySelectorAll(".nav-links a");

burger.addEventListener("click", () => {

    console.log("Test1");
    otherNav.classList.toggle('menu-appear');
    // navlinks.classList.toggle('navLinkFade');
    burger.classList.toggle("toggle");

 });

//  //
//};
//}
//navSlide();

//function openPopup(event){
//     console.log("Contains Poster Quote")
//};

//    const popCont = document.querySelector('.pop-cont');
//    popup.classList.add("show-popup");

//Read Form
$(document).ready(function(){

    $('.pop-btns').click(function(){
//        console.log('Cleicked');
        $('form').serializeArray();
        $('form').submit();
    })
});


function closePopup(){
    popup.classList.remove("show-popup");
    popCont.forEach(function(div){
        div.classList.remove("show-popup");
    })
}

//function boolOptionsFunc(){

var boolOpts = document.querySelectorAll(".bool-options");

boolOpts.forEach(function(elem){

    elem.addEventListener('click', function(event){

        if (event.target.classList.contains("activate-options")){
//              console.log("Clicked: ",event.target.style.color);
              elem.classList.remove("activate-options");
              elem.classList.add("bool-options");
        }else{
//            console.log("Click: ",event.target);
            elem.classList.add("activate-options");
            elem.classList.remove("bool-options");
        }
    });

});

//}

//window.addEventListener('click', function(event){
//    if(popup){
//        if(event.target != popCont){
//           popup.classList.remove(".show");
//        }
//    }
//});

if (currentSectionIndex == 0){
    firstSection.style.display = "block";

    changeProgressColor()

    }else{
        firstSection.style.display = "none";
};


function showNextSection() {

    //Prevents Current Page From Reloading
    event.preventDefault();

    sections[currentSectionIndex].style.display = "none"; // Hide current section
    currentSectionIndex++; // Move to the next section

    if (currentSectionIndex < sections.length) {
        sections[currentSectionIndex].style.display = "block"; // Show next section
        changeProgressColor()
        };

    };



//observer.observe()

//
//function showPreviousSection() {
//
//    //Prevents Page From Reloading
//    event.preventDefault();
//
//    sections[currentSectionIndex].style.display = "none"; // Hide current section
//    currentSectionIndex--; // Move to the next section
//
//    if (currentSectionIndex >= 0) {
//        sections[currentSectionIndex].style.display = "block"; // Show next section
//        //changeProgressColor()
//        };
//
//    };

//function showPreviousSection() {
//
//    history.go(-1)
//
//
//
//    };



//If Other in web type is selected do the following...
document.querySelector("#otherType").addEventListener('change',function(e){

        if (this.selectedIndex == 5){
            var anInput = document.createElement('input');
            var otherLabel = document.createElement('label');
            var parent = this.parentNode;
            //Assign IDs
            anInput.id = 'other-opt-input';
            otherLabel.id = 'other-opt-label';
            // Label description
            otherLabel.innerHTML = '<span> Please Specify: </span> '
            //Add Class
            anInput.classList.add('form-control-other');
            parent.appendChild(otherLabel);
            this.parentNode.appendChild(anInput);

        }else{
            //If these Elements are defined/present, remove them
            if(document.querySelector("#other-opt-input") != "undefined"){
                document.querySelector("#other-opt-input").remove();
                document.querySelector("#other-opt-label").remove();
            }

        }

    });


    //If Other in web type is selected do the following...
document.querySelector("#checkbox-opt").addEventListener('change',function(){

        if (this.checked){
            var anInput = document.createElement('input');
            var otherLabel = document.createElement('label');
            var parent = this.parentNode;
            //Assign IDs
            anInput.id = 'doc-upload-id';
            anInput.type = 'file';
            otherLabel.id = 'doc-upload-label';
            // Label description
            otherLabel.innerHTML = '<br><br><span> Please Upload Document below: </span> <br><br> '
            //Add Class
            //anInput.classList.add('form-control-other');
            parent.appendChild(otherLabel);
            this.parentNode.appendChild(anInput);

        }else{
            //If these Elements are defined/present, remove them
            if(document.querySelector("#doc-upload-id") != "undefined"){
                document.querySelector("#doc-upload-id").remove();
                document.querySelector("#doc-upload-label").remove();
            }

        }

    }
    );

var $message = $('.sel-tag');

$(window).on('mousemove', function(e) {
    if(e.clientX > e.clientY) {
        $message.text('top right triangle');
    } else {
        $message.text('bottom left triangle');
    }
});

var closeDraw = document.querySelector('#close-draw');
// var sideNavCont = document.querySelector("#side-navig-cont");

function closeDraw(){
    console.log("A Click");
    let sideNavBg = document.querySelector('#side-navig-bg');
    let sideNavCont = document.querySelector("#side-navig-cont");
    // document.querySelector("#commentField").value = "";
    sideNavBg.classList.toggle("show-popup");
    sideNavCont.classList.toggle("show-menu");
};

function sideNavFunc(event){
    // var popScrnLogo = document.getElementById("updates");
    // popScrnLogo.classList.toggle("show-popup");
    console.log("Side Nav");
    let sideNavBg = document.querySelector('#side-navig-bg');
    let sideNavCont = document.querySelector("#side-navig-cont");
    // document.querySelector("#commentField").value = "";
    sideNavBg.classList.toggle("show-popup");
    sideNavCont.classList.toggle("show-menu");

    };

    
function closeSideNavFunc(){
    // var popScrnLogo = document.getElementById("updates");
    // popScrnLogo.classList.toggle("show-popup");
    console.log("Side Nav");
    let sideNavBg = document.querySelector('#side-navig-bg');
    let sideNavCont = document.querySelector("#side-navig-cont");
    // document.querySelector("#commentField").value = "";
    sideNavBg.classList.remove("show-popup");
    sideNavCont.classList.remove("show-menu");
    };
    

    function showHideFbtns(){
        let fbtns = document.querySelector('#stats-cont');
        let contHandle = document.querySelector('#cont-handle');
        fbtns.classList.toggle('show-it');
        contHandle.classList.toggle('rotate-45');
        // contHandle.style.transitionDelay = '0.3s'
    }

    function showHideOfferings(id){
        let OfferingCont = document.querySelector("#offering-cont-" +id); 
        let contHandle = document.querySelector('#cont-handle-' + id);
        OfferingCont.classList.toggle('show-it');
        contHandle.classList.toggle('rotate-45');
    }

    function showHideSermons(id){
        let OfferingCont = document.querySelector("#sermon-cont-" +id); 
        let contHandle = document.querySelector('#conta-handle-' + id);
        OfferingCont.classList.toggle('show-it');
        contHandle.classList.toggle('rotate-45');
    }

    function showHideMinutes(id){
        let OfferingCont = document.querySelector("#minutes-cont-" +id); 
        let contHandle = document.querySelector('#conta-handle-' + id);
        OfferingCont.classList.toggle('show-it');
        contHandle.classList.toggle('rotate-45');
    }


   