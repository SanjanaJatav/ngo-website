/*
===========================================
NGO Website - Main JavaScript
Interactive features and animations
===========================================
*/

(function($) {
    'use strict';

    /* ===========================================
       DOM READY INITIALIZATION
    =========================================== */
    $(document).ready(function() {
        initHeroSlider();
        initScrollEffects();
        initAnimatedCounters();
        initFormValidation();
        initScrollToTop();
        initLazyLoading();
        initFilterFunctionality();
        initLightbox();
    });

    /* ===========================================
       HERO IMAGE SLIDER
    =========================================== */
    function initHeroSlider() {
        const $slider = $('.hero-slider');
        if ($slider.length === 0) return;

        const $slides = $('.hero-slide');
        const $indicators = $('.slider-indicator');
        let currentSlide = 0;
        let sliderInterval;

        // Show first slide
        $slides.eq(0).addClass('active');
        $indicators.eq(0).addClass('active');

        function showSlide(index) {
            $slides.removeClass('active');
            $indicators.removeClass('active');
            
            $slides.eq(index).addClass('active');
            $indicators.eq(index).addClass('active');
            
            currentSlide = index;
        }

        function nextSlide() {
            let next = (currentSlide + 1) % $slides.length;
            showSlide(next);
        }

        function startSlider() {
            sliderInterval = setInterval(nextSlide, 5000); // 5 seconds
        }

        function stopSlider() {
            clearInterval(sliderInterval);
        }

        // Indicator click handlers
        $indicators.on('click', function() {
            const index = $(this).index();
            showSlide(index);
            stopSlider();
            startSlider();
        });

        // Pause on hover
        $slider.on('mouseenter', stopSlider);
        $slider.on('mouseleave', startSlider);

        // Start automatic sliding
        startSlider();
    }

    /* ===========================================
       SCROLL EFFECTS
    =========================================== */
    function initScrollEffects() {
        const $navbar = $('.navbar');
        
        $(window).on('scroll', function() {
            if ($(this).scrollTop() > 50) {
                $navbar.addClass('scrolled');
            } else {
                $navbar.removeClass('scrolled');
            }
        });

        // Smooth scroll for anchor links
        $('a[href^="#"]').on('click', function(e) {
            const target = $(this.getAttribute('href'));
            if (target.length) {
                e.preventDefault();
                $('html, body').stop().animate({
                    scrollTop: target.offset().top - 80
                }, 1000);
            }
        });
    }

    /* ===========================================
       ANIMATED COUNTERS (Statistics)
    =========================================== */
    function initAnimatedCounters() {
        const $counters = $('.stat-number');
        if ($counters.length === 0) return;

        let hasAnimated = false;

        // Intersection Observer for triggering animation when visible
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting && !hasAnimated) {
                        hasAnimated = true;
                        animateCounters();
                    }
                });
            }, { threshold: 0.5 });

            const statsSection = document.querySelector('.stats-section');
            if (statsSection) {
                observer.observe(statsSection);
            }
        } else {
            // Fallback for browsers without Intersection Observer
            $(window).on('scroll', function() {
                const statsSection = $('.stats-section');
                if (statsSection.length && !hasAnimated) {
                    const sectionTop = statsSection.offset().top;
                    const scrollTop = $(window).scrollTop();
                    const windowHeight = $(window).height();

                    if (scrollTop + windowHeight > sectionTop + 100) {
                        hasAnimated = true;
                        animateCounters();
                    }
                }
            });
        }

        function animateCounters() {
            $counters.each(function() {
                const $counter = $(this);
                const target = parseInt($counter.attr('data-target')) || parseInt($counter.text().replace(/,/g, ''));
                const duration = 2000; // 2 seconds
                const increment = target / (duration / 16); // 60fps

                let current = 0;
                $counter.text('0');

                const updateCounter = function() {
                    current += increment;
                    if (current < target) {
                        $counter.text(Math.floor(current).toLocaleString());
                        requestAnimationFrame(updateCounter);
                    } else {
                        $counter.text(target.toLocaleString());
                    }
                };

                requestAnimationFrame(updateCounter);
            });
        }
    }

    /* ===========================================
       FORM VALIDATION
    =========================================== */
    function initFormValidation() {
        $('form').on('submit', function(e) {
            let isValid = true;
            const $form = $(this);

            // Clear previous errors
            $form.find('.error-message').remove();
            $form.find('.is-invalid').removeClass('is-invalid');

            // Validate required fields
            $form.find('[required]').each(function() {
                const $field = $(this);
                const value = $field.val().trim();

                if (!value) {
                    isValid = false;
                    markFieldInvalid($field, 'This field is required');
                }
            });

            // Validate email fields
            $form.find('input[type="email"]').each(function() {
                const $field = $(this);
                const email = $field.val().trim();

                if (email && !isValidEmail(email)) {
                    isValid = false;
                    markFieldInvalid($field, 'Please enter a valid email address');
                }
            });

            // Validate phone numbers
            $form.find('input[type="tel"], input[name*="phone"]').each(function() {
                const $field = $(this);
                const phone = $field.val().trim();

                if (phone && !isValidPhone(phone)) {
                    isValid = false;
                    markFieldInvalid($field, 'Please enter a valid phone number');
                }
            });

            // Validate donation amount
            const $amountField = $form.find('input[name="amount"]');
            if ($amountField.length) {
                const amount = parseFloat($amountField.val());
                const minDonation = parseInt($amountField.attr('data-min')) || 100;

                if (isNaN(amount) || amount < minDonation) {
                    isValid = false;
                    markFieldInvalid($amountField, `Minimum donation amount is ₹${minDonation}`);
                }
            }

            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const $firstError = $form.find('.is-invalid').first();
                if ($firstError.length) {
                    $('html, body').animate({
                        scrollTop: $firstError.offset().top - 100
                    }, 500);
                }
            }
        });

        // Real-time validation on blur
        $('input[required], input[type="email"], input[type="tel"]').on('blur', function() {
            const $field = $(this);
            const value = $field.val().trim();

            // Remove previous error
            $field.removeClass('is-invalid');
            $field.next('.error-message').remove();

            // Validate
            if ($field.attr('required') && !value) {
                markFieldInvalid($field, 'This field is required');
            } else if ($field.attr('type') === 'email' && value && !isValidEmail(value)) {
                markFieldInvalid($field, 'Please enter a valid email address');
            } else if (($field.attr('type') === 'tel' || $field.attr('name').includes('phone')) && value && !isValidPhone(value)) {
                markFieldInvalid($field, 'Please enter a valid phone number');
            }
        });

        function markFieldInvalid($field, message) {
            $field.addClass('is-invalid');
            $field.after(`<div class="error-message text-danger mt-1"><small>${message}</small></div>`);
        }

        function isValidEmail(email) {
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return regex.test(email);
        }

        function isValidPhone(phone) {
            const regex = /^[\d\s\-\+\(\)]{10,}$/;
            return regex.test(phone);
        }
    }

    /* ===========================================
       SCROLL TO TOP BUTTON
    =========================================== */
    function initScrollToTop() {
        const $scrollBtn = $('#scrollTopBtn');

        $(window).on('scroll', function() {
            if ($(this).scrollTop() > 300) {
                $scrollBtn.addClass('show');
            } else {
                $scrollBtn.removeClass('show');
            }
        });

        $scrollBtn.on('click', function() {
            $('html, body').animate({ scrollTop: 0 }, 800);
        });
    }

    /* ===========================================
       LAZY LOADING FOR IMAGES
    =========================================== */
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(function(img) {
                imageObserver.observe(img);
            });
        } else {
            // Fallback for browsers without Intersection Observer
            $('img[data-src]').each(function() {
                $(this).attr('src', $(this).data('src'));
            });
        }
    }

    /* ===========================================
       FILTER FUNCTIONALITY (Projects/Media)
    =========================================== */
    function initFilterFunctionality() {
        $('.filter-btn').on('click', function() {
            const $btn = $(this);
            const filter = $btn.data('filter');
            
            // Update active state
            $('.filter-btn').removeClass('active');
            $btn.addClass('active');

            // Filter items
            if (filter === 'all') {
                $('.filter-item').fadeIn(400);
            } else {
                $('.filter-item').hide();
                $(`.filter-item[data-category="${filter}"]`).fadeIn(400);
            }
        });

        // Category filter dropdowns (if using select elements)
        $('select[name="category"], select[name="media_type"]').on('change', function() {
            const $form = $(this).closest('form');
            const baseUrl = window.location.pathname;
            const category = $('select[name="category"]').val() || 'all';
            const mediaType = $('select[name="media_type"]').val() || 'all';
            
            // Build query string
            let params = [];
            if (category !== 'all') params.push(`category=${category}`);
            if (mediaType !== 'all') params.push(`media_type=${mediaType}`);
            
            const queryString = params.length ? '?' + params.join('&') : '';
            window.location.href = baseUrl + queryString;
        });
    }

    /* ===========================================
       LIGHTBOX FOR IMAGES
    =========================================== */
    function initLightbox() {
        const $lightbox = $(`
            <div class="lightbox" style="display: none;">
                <div class="lightbox-overlay"></div>
                <div class="lightbox-content">
                    <button class="lightbox-close">&times;</button>
                    <img class="lightbox-image" src="" alt="">
                    <button class="lightbox-prev">&lsaquo;</button>
                    <button class="lightbox-next">&rsaquo;</button>
                </div>
            </div>
        `);

        $('body').append($lightbox);

        let currentImageIndex = 0;
        let $images = [];

        // Open lightbox on image click
        $(document).on('click', '.gallery-image, .media-item img', function(e) {
            e.preventDefault();
            const $clickedImg = $(this);
            
            // Get all gallery images
            $images = $('.gallery-image, .media-item img');
            currentImageIndex = $images.index($clickedImg);

            showLightboxImage(currentImageIndex);
            $lightbox.fadeIn(300);
            $('body').css('overflow', 'hidden');
        });

        function showLightboxImage(index) {
            const $img = $images.eq(index);
            const src = $img.attr('src') || $img.attr('data-src');
            $('.lightbox-image').attr('src', src);
            currentImageIndex = index;

            // Show/hide navigation buttons
            if ($images.length <= 1) {
                $('.lightbox-prev, .lightbox-next').hide();
            } else {
                $('.lightbox-prev, .lightbox-next').show();
            }
        }

        // Close lightbox
        $('.lightbox-close, .lightbox-overlay').on('click', function() {
            $lightbox.fadeOut(300);
            $('body').css('overflow', '');
        });

        // Navigation
        $('.lightbox-prev').on('click', function() {
            currentImageIndex = (currentImageIndex - 1 + $images.length) % $images.length;
            showLightboxImage(currentImageIndex);
        });

        $('.lightbox-next').on('click', function() {
            currentImageIndex = (currentImageIndex + 1) % $images.length;
            showLightboxImage(currentImageIndex);
        });

        // Keyboard navigation
        $(document).on('keydown', function(e) {
            if ($lightbox.is(':visible')) {
                if (e.key === 'Escape') {
                    $lightbox.fadeOut(300);
                    $('body').css('overflow', '');
                } else if (e.key === 'ArrowLeft') {
                    $('.lightbox-prev').click();
                } else if (e.key === 'ArrowRight') {
                    $('.lightbox-next').click();
                }
            }
        });
    }

    /* ===========================================
       DONATION FORM - AMOUNT SELECTION
    =========================================== */
    $('.amount-option').on('click', function() {
        $('.amount-option').removeClass('selected');
        $(this).addClass('selected');
        const amount = $(this).data('amount');
        $('input[name="amount"]').val(amount);
    });

    // Custom amount input
    $('input[name="amount"]').on('input', function() {
        $('.amount-option').removeClass('selected');
    });

    /* ===========================================
       UPI APP SELECTION
    =========================================== */
    $('.upi-app-option').on('click', function() {
        $('.upi-app-option').removeClass('selected');
        $(this).addClass('selected');
        const app = $(this).data('app');
        $('input[name="payment_app"]').val(app);
    });

    /* ===========================================
       FADE-IN ELEMENTS ON SCROLL
    =========================================== */
    function initScrollAnimations() {
        if ('IntersectionObserver' in window) {
            const animateObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-fade-in-up');
                        animateObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            document.querySelectorAll('.card, .project-card, .stat-card').forEach(function(el) {
                animateObserver.observe(el);
            });
        }
    }

    initScrollAnimations();

})(jQuery);

/* ===========================================
   LIGHTBOX STYLES (injected via JS)
=========================================== */
const lightboxStyles = `
<style>
.lightbox {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9999;
}

.lightbox-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.95);
}

.lightbox-content {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.lightbox-image {
    max-width: 90%;
    max-height: 90%;
    object-fit: contain;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.lightbox-close {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border: none;
    border-radius: 50%;
    color: white;
    font-size: 2rem;
    cursor: pointer;
    transition: all 0.3s;
    z-index: 10;
}

.lightbox-close:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: rotate(90deg);
}

.lightbox-prev,
.lightbox-next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 50px;
    height: 50px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border: none;
    border-radius: 50%;
    color: white;
    font-size: 2rem;
    cursor: pointer;
    transition: all 0.3s;
    z-index: 10;
}

.lightbox-prev {
    left: 20px;
}

.lightbox-next {
    right: 20px;
}

.lightbox-prev:hover,
.lightbox-next:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-50%) scale(1.1);
}

@media (max-width: 768px) {
    .lightbox-image {
        max-width: 95%;
        max-height: 80%;
    }
    
    .lightbox-prev,
    .lightbox-next {
        width: 40px;
        height: 40px;
        font-size: 1.5rem;
    }
    
    .lightbox-prev {
        left: 10px;
    }
    
    .lightbox-next {
        right: 10px;
    }
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', lightboxStyles);
