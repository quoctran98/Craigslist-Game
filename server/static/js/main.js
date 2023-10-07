// Fetch random listings and populate id-"listing-left" and id-"listing-right"

function format_price(price) {
    let formatted_price = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    if (formatted_price.indexOf(".") !== -1) {
        if (formatted_price.split(".")[1] === "00") {
            formatted_price = formatted_price.split(".")[0];
        }
    }
    return(formatted_price);
}

let LEFT_LISTING = null;
let RIGHT_LISTING = null;
let score = 0;

function render_listing(data) {
    html = `
    <div class="listing-box__image">
        <div class="listing-box__price" style="display: none;">
            <h1>$${format_price(data.price)}</h1>
        </div>
        <img src="${data.image[0]}" alt="listing image">
    </div>
    <div class="listing-box__title">
        <h3>${data.name}</h3>
    </div>
    <div class="listing-box__location">
        <h5>${data.location.addressLocality}, ${data.location.addressRegion}</h5></div>
    </div>
    `;
    return(html);
}

async function next_listing() {
    // Clear the result
    $("#result").html("");

    // Move right listing to left
    $("#listing-left").html($("#listing-right").html());
    $(".listing-box__image img").css("filter", "blur(0px)");
    $("#listing-left").click(function() {
        make_guess("left");
    });
    LEFT_LISTING = RIGHT_LISTING;

    // Fetch new right listing
    fetch("/api/random_listing", {method: 'GET'})
    .then(response => response.json())
    .then(data => {
        $("#listing-right").html(render_listing(data[0]));
        $("#listing-right").click(function() {
            make_guess("right");
        });
        RIGHT_LISTING = data[0];
    });
}

function make_guess(guess) {

    // Disable clicking
    $("#listing-left").off("click");
    $("#listing-right").off("click");

    const left_price = parseFloat(LEFT_LISTING.price);
    const right_price = parseFloat(RIGHT_LISTING.price);

    let correct = false;
    if (guess === "left" && left_price >= right_price) {
        correct = true;
    } else if (guess === "right" && left_price <= right_price) {
        correct = true;
    }

    if (correct) {
        score += 1;
    } else {
        score = 0;
    }

    console.log(LEFT_LISTING.price);
    console.log(RIGHT_LISTING.price);
    console.log(guess);

    // Display prices and blur image
    $("#listing-left .listing-box__price").show();
    $("#listing-right .listing-box__price").show();
    $(".listing-box__image img").css("filter", "blur(5px)");

    // Display correct or incorrect
    $("#result").html(correct ? "Correct!" : "Incorrect!");
    $("#result").css("color", correct ? "green" : "red");
    $("#score").html(score);
}

fetch(`/api/random_listing?n=${2}`, {method: 'GET'})
.then(response => response.json())
.then(data => {
    console.log(data);
    $("#listing-left").html(render_listing(data[0]));
    $("#listing-right").html(render_listing(data[1]));

    LEFT_LISTING = data[0];
    RIGHT_LISTING = data[1];

    $("#listing-left").click(function() {
        make_guess("left");
    });
    $("#listing-right").click(function() {
        make_guess("right");
    });
});

function display_listings(listings) {
    // display the last two listings on the left and right
    $("#listing-left").html(render_listing(listings[0]));
    $("#listing-right").html(render_listing(listings[1]));

    // add the event listeners to the listings
    $("#listing-left").click(function() {
        make_guess("left");
    });
    $("#listing-right").click(function() {
        make_guess("right");
    });
}

function game_loop(categories) {
    let score = 0;
    let streak = 0;
    let oopsies = 0;

    let all_listings = [];

    // fetch the two listings to start the game
    encoded_cats = encodeURIComponent(JSON.stringify(categories));
    fetch(`/api/random_listing?n=${2}?categories=${encoded_cats}`, {method: 'GET'})
    .then(response => response.json())
    .then(data => {
        all_listings = data;
    });

    

}