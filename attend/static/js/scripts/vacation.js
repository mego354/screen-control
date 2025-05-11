var numberOfStars = 200;
        
for (var i = 0; i < numberOfStars; i++) {
    var blob = document.createElement('div');
    blob.classList.add('blob', 'fa', 'fa-star', i.toString());
    document.querySelector('.vacation_container').appendChild(blob);
}

animateText();
animateBlobs();

document.querySelector('.vacation_container').addEventListener('click', function() {
reset();
animateText();
animateBlobs();
});

function reset() {
document.querySelectorAll('.blob').forEach(function(blob) {
    gsap.set(blob, { x: 0, y: 0, opacity: 1 });
});

gsap.set(document.querySelector('#vacation_h1'), { scale: 1, opacity: 1, rotation: 0 });
}

function animateText() {
    gsap.from(document.querySelector('#vacation_h1'), {
        duration: 0.8,
        scale: 0.4,
        opacity: 0,
        rotation: 15,
        ease: "back.out(4)"
    });
}

function animateBlobs() {
    // Get screen width
    var screenWidth = window.innerWidth;

    if (screenWidth > 768) {
        var xSeed = random(350, 380);
        var ySeed = random(120, 170);
    }
    else if (screenWidth > 425) {
        var xSeed = random(280, 350);
        var ySeed = random(120, 170);
    }
    else if (screenWidth >= 375) {
        var xSeed = random(120, 155);
        var ySeed = random(120, 170);
    }
    else {
        var xSeed = random(90, 110);
        var ySeed = random(120, 150);
    }

    document.querySelectorAll('.blob').forEach(function(blob) {
        var speed = random(1, 5);
        var rotation = random(5, 100);
        var scale = random(0.8, 1.5);
        var x = random(-xSeed, xSeed);
        var y = random(-ySeed, ySeed);

        gsap.to(blob, {
            duration: speed,
            x: x,
            y: y,
            ease: "power1.out",
            opacity: 0,
            rotation: rotation,
            scale: scale,
            onStart: function() {
                blob.style.display = 'block';
            },
            onComplete: function() {
                blob.style.display = 'none';
            }
        });
    });
}

function random(min, max) {
    return Math.random() * (max - min) + min;
}
