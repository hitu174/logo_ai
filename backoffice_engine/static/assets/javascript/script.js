/*------------------------------------- Page Loader -------------------------------------*/
$(function () {
    setTimeout(() => {
        $('.page-loader').fadeOut('slow');
    }, 500);
});
/*------------------------------------- Sticky Header -------------------------------------*/
$(document).ready(function () {
    $(window).scroll(function () {
        var scrollPosition = $(window).scrollTop();
        if (scrollPosition >= 20) {
            $('#top-header, #top-navbar').addClass('fixed');
        } else {
            $('#top-header, #top-navbar').removeClass('fixed');
        }
    });
});
/*------------------------------------- Toggle Header Menu -------------------------------------*/
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links-mn');
    const overlay = document.querySelector('.overlay');

    if (navLinks.classList.contains('active')) {
        navLinks.classList.add('closing');
        overlay.classList.remove('active');
        setTimeout(() => {
            navLinks.classList.remove('active', 'closing');
        }, 300);
    } else {
        navLinks.classList.remove('closing');
        navLinks.classList.add('active');
        overlay.classList.add('active');
    }
}

// Close menu when clicking outside
document.addEventListener('click', function (event) {
    const navLinks = document.querySelector('.nav-links-mn');
    const overlay = document.querySelector('.overlay');
    const menuIcon = document.querySelector('.menu-icon');

    if (
        !navLinks.contains(event.target) &&
        !menuIcon.contains(event.target) &&
        overlay.classList.contains('active')
    ) {
        toggleMenu();
    }
});

/*------------------------------------- Select all dropdown menus -------------------------------------*/
const optionMenus = document.querySelectorAll(".select-menu");
optionMenus.forEach((optionMenu) => {
    const selectBtn = optionMenu.querySelector(".select-btn");
    const options = optionMenu.querySelectorAll(".option");

    selectBtn.addEventListener("click", () => {

        optionMenus.forEach((menu) => {
            if (menu !== optionMenu) {
                menu.classList.remove("active");
            }
        });
        optionMenu.classList.toggle("active");
    });

    options.forEach((option) => {
        option.addEventListener("click", () => {
            optionMenu.classList.remove("active");
        });
    });
});

document.addEventListener("click", (event) => {
    if (!event.target.closest(".select-menu")) {
        optionMenus.forEach((optionMenu) => {
            optionMenu.classList.remove("active");
        });
    }
});

/*------------- Shop Slider Home Screen ---------------------*/
$(document).ready(function () {
    $('.photo-gallery').slick({
        infinity: true,
        slidesToShow: 6,
        slidesToScroll: 1,
        autoplay: true,
        arrows: false,
        dots: false,
        speed: 1000,
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            }
        ]
    });
});

/*------------- Suggestion Slider ---------------------*/
$(document).ready(function () {
    $('.wrapper').slick({
        infinity: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        arrows: false,
        dots: false,
        speed: 1000,
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    arrows: false,
                }
            }
        ]
    });
});

/*------------- custom-cursor ---------------------*/
document.addEventListener("DOMContentLoaded", function () {
    const cursor = document.createElement("div");
    cursor.classList.add("custom-cursor");

    const arrowImg = document.createElement("img");
    arrowImg.src = "assets/images/svg/arrow-bar-both.svg";
    arrowImg.classList.add("cursor-arrow");

    cursor.appendChild(arrowImg);
    document.body.appendChild(cursor);

    const suggBoxes = document.querySelectorAll(".cursor");

    suggBoxes.forEach((box) => {
        box.addEventListener("mouseenter", () => {
            cursor.style.display = "block";
        });

        box.addEventListener("mouseleave", () => {
            cursor.style.display = "none";
        });

        box.addEventListener("mousemove", (e) => {
            cursor.style.left = `${e.clientX}px`;
            cursor.style.top = `${e.clientY}px`;
        });
    });
});


/*------------------------------------- Infinite Marquee -------------------------------------*/
document.querySelectorAll('.logos').forEach(function (logosContainer) {
    const copy = logosContainer.querySelector('.logos-slide').cloneNode(true);
    logosContainer.appendChild(copy);
});

/*------------- sayAboutSlider ---------------------*/
$(document).ready(function () {
    $('.sayAboutSlider').slick({
        infinity: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        arrows: true,
        dots: false,
        speed: 1000,
        prevArrow: '<button type="button" class="single-slick-arrow slick-prev"><img src="assets/images/svg/white-left-arrow.svg" alt="left-black-arrow"></button>',
        nextArrow: '<button type="button" class="single-slick-arrow slick-next"><img src="assets/images/svg/white-right-arrow.svg" alt="right-half-arrow"></button>',
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    arrows: false,
                }
            }
        ]
    });
});

/*------------------------------------- Pricing Tabs btn -------------------------------------*/
$(function () {
    $('.tabs-btn').on('click', 'a', function () {
        var tabId = $(this).attr('data-tab');

        $('.tabs-btn a').removeClass('active');
        $('.Tabcondent').removeClass('active');

        $(this).addClass('active');
        $('#' + tabId).addClass('active');
    });
});

/*------------------------------------- Active Page Active Menu -------------------------------------*/
document.addEventListener("DOMContentLoaded", function () {
    let currentPage = window.location.pathname.split("/").pop();
    let menuLinks = document.querySelectorAll(".a-link");
    let selectMenus = document.querySelectorAll(".select-menu");

    menuLinks.forEach(link => {
        let linkHref = link.getAttribute("href");

        if (currentPage === linkHref) {
            link.classList.add("active");

            let parentMenu = link.closest(".select-menu");
            if (parentMenu) {
                parentMenu.querySelector(".select-btn").classList.add("active");
            }
        }
    });
});
/*------------------------------------- Form Change Toggle -------------------------------------*/
const toggleForm = () => {
    const container = document.querySelector('.container-demo');
    container.classList.toggle('active');
};

/*------------------------------------- Bottom To Top Button -------------------------------------*/
window.addEventListener('scroll', function () {
    var button = document.querySelector('.bottom-top-button');
    if (window.pageYOffset > 100) {
        button.style.display = 'block';

    } else {
        button.style.display = 'none';
    }
});

document.querySelector('.bottom-top-button').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});