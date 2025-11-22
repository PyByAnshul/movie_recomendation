// getting all required elements
const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
const icon = searchWrapper.querySelector(".icon");
let linkTag = searchWrapper.querySelector("a");
let webLink;

// if user press any key and release
inputBox.onkeyup = (e) => {
    let userData = e.target.value; //user enetered data
    let emptyArray = [];
    if (userData) {
        let data = userData
        var params = { user_input: data }
        var xhrr = new XMLHttpRequest()

        xhrr.open('post', '../update', true)
        xhrr.setRequestHeader('Content-type', 'application/json')
        xhrr.onload = function stt() {



            let suggestions = JSON.parse(this.responseText)
            console.log(suggestions)
            emptyArray = suggestions.filter((data) => {

                //filtering array value and user characters to lowercase and return only those words which are start with user enetered chars
                return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
            });
            emptyArray = emptyArray.map((data) => {
                // passing return data inside li tag
                return data = `<li>${data}</li>`;
            });
            searchWrapper.classList.add("active"); //show autocomplete box
            showSuggestions(emptyArray);
            let allList = suggBox.querySelectorAll("li");
            for (let i = 0; i < allList.length; i++) {
                //adding onclick attribute in all li tag
                allList[i].setAttribute("onclick", "select(this)");
            }

            //document.getElementById('prediction').innerHTML= this.responseText;

        }
        xhrr.send(JSON.stringify(params));

    } else {
        searchWrapper.classList.remove("active"); //hide autocomplete box
    }
}

function select(element) {

    let selectData = element.textContent;
    inputBox.value = selectData;
    
    icon.onclick = () => {
        var x = document.getElementById('container_section_wrapper')
        x.style.display = "none"
        var container = document.getElementById('container_section');
        container.style.display = "none";
        var x = document.getElementById('container_section3');
        x.style.display = "flex"
        for (var i = 0; i < 4; i++) {
            displaywrapper_movies()
        }
        var container = document.getElementById('container_section2');



        var params = { text_data: selectData };
        var xhrr = new XMLHttpRequest()

        xhrr.open('post', '../gettext', true)
        xhrr.setRequestHeader('Content-type', 'application/json')
        xhrr.onload = function () {
            if (xhrr.readyState == 4 && xhrr.status == 200) {
                x.style.display = "none"
                container.style.display = "flex";
                let arr = JSON.parse(this.responseText)

                for (var i = 0; i < arr.length; i++) {
                    var obj = arr[i];
                    // Fetch poster asynchronously
                    fetchPosterAndDisplay(obj.title, obj.overview, obj.movie_id, displaymovies);
                }
            }




            //document.getElementById('prediction').innerHTML= this.responseText;
        }
        xhrr.send(JSON.stringify(params))

    }
    searchWrapper.classList.remove("active");
}

function showSuggestions(list) {
    let listData;
    if (!list.length) {
        userValue = inputBox.value;
        listData = `<li>${userValue}</li>`;
    } else {
        listData = list.join('');
    }
    suggBox.innerHTML = listData;
}



function displaytask(title, description, image) {
    // get the container 
    var container = document.querySelector('.container_section');


    // create dynamic content
    let p = `
    <div class="card_container">

            <div class="card">
                <img src="${image}" alt="">

            </div>
            <div class="card__content">
                <p class="card__title">${title}
                </p>
                <p class="card__description">${description}</p>

            </div>
        </div>
 
    
`;
    // insert dynamic content in container
    container.insertAdjacentHTML("beforeend", p)
    // this function is use to element using id to element

}

window.onload = function () {

    var x = document.getElementById('container_section_wrapper')
    var container = document.getElementById('container_section');
    container.style.display = "none";
    for (var i = 0; i < 12; i++) {
        displaywrapper()
    }

    var xhrr = new XMLHttpRequest()


    xhrr.open('get', '../movies_data', true)
    xhrr.setRequestHeader('Content-type', 'application/json')
    xhrr.onload = function () {

        if (xhrr.readyState == 4 && xhrr.status == 200) {
            x.style.display = "none"
            container.style.display = "flex";
            let arr = JSON.parse(this.responseText)

            for (var i = 0; i < arr.length; i++) {
                var obj = arr[i];
                // Fetch poster asynchronously
                fetchPosterAndDisplay(obj.title, obj.tags, obj.movie_id, displaytask);
            }
        }



        //document.getElementById('prediction').innerHTML= this.responseText;
    }
    xhrr.send()
}


window.onscroll = function (ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight + 126) {
        var xhrr = new XMLHttpRequest()

        xhrr.open('get', '../movies_data', true)
        xhrr.setRequestHeader('Content-type', 'application/json')
        xhrr.onload = function () {
            let arr = JSON.parse(this.responseText)

            for (var i = 0; i < arr.length; i++) {
                var obj = arr[i];
                // Fetch poster asynchronously
                fetchPosterAndDisplay(obj.title, obj.tags, obj.movie_id, displaytask);
            }
        }
        xhrr.send()
    }
};


function displaymovies(title, description, image) {
    // get the container 
    var container = document.querySelector('.container_section2');


    // create dynamic content
    let q = `
  
    <div class="main_container">
    <div class="image_container">
        <img class="hset" src="${image}">
                       
    </div>

    <div class="details">
        <h1 class="title"><span style="color: #252629;">${title}</span></h1>
        <p>${description}</p>

    </div>
</div>
    
`;
    // insert dynamic content in container
    container.insertAdjacentHTML("beforeend", q)
    // this function is use to element using id to element

}

function displaywrapper() {
    // get the container 
    var container = document.querySelector('.container_section_wrapper');


    // create dynamic content
    let q = `
  
    <div class="loader">
    <div class="wrapper">
      <div class="circle"></div>
      <div class="line-1"></div>
      <div class="line-2"></div>
      <div class="line-3"></div>
      <div class="line-4"></div>
    </div>
  </div>
    
`;
    // insert dynamic content in container
    container.insertAdjacentHTML("beforeend", q)
    // this function is use to element using id to element

}

function displaywrapper_movies() {
    // get the container 
    var container = document.querySelector('.container_section3');


    // create dynamic content
    let q = `
  
    <div class="main_containers">
            <div class="image_containers">
                <div class="loaders"></div>
            </div>

            <div class="details">
                <div class="line-1s"></div>
                    
                
                    <div class="line-2s"></div>
                

            </div>
        </div>
    
`;
    // insert dynamic content in container
    container.insertAdjacentHTML("beforeend", q)
    // this function is use to element using id to element

}

// Function to fetch poster asynchronously
function fetchPosterAndDisplay(title, description, movieId, displayFunction) {
    // Show placeholder first
    displayFunction(title, description, "https://via.placeholder.com/500x750?text=Loading...");
    
    // Fetch poster asynchronously
    fetch(`https://api.themoviedb.org/3/movie/${movieId}?api_key=a27a49bf043d4a93c59dccc8ffde1312&language=en-US`)
        .then(response => response.json())
        .then(data => {
            if (data.poster_path) {
                const posterUrl = `https://image.tmdb.org/t/p/w500${data.poster_path}`;
                // Update the image src
                updateMovieImage(title, posterUrl);
            }
        })
        .catch(error => {
            console.log('Error fetching poster:', error);
            updateMovieImage(title, "https://via.placeholder.com/500x750?text=No+Image");
        });
}

// Function to update movie image after async fetch
function updateMovieImage(title, imageUrl) {
    // Find all images and update the one with matching title
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        const container = img.closest('.card_container, .main_container');
        if (container) {
            const titleElement = container.querySelector('.card__title, .title');
            if (titleElement && titleElement.textContent.trim() === title) {
                img.src = imageUrl;
            }
        }
    });
}