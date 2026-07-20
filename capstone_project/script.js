/* =====================================
   AI Resume Screener - script.js
===================================== */


/* =====================================
   Dark / Light Mode
===================================== */

const themeToggle = document.getElementById("themeToggle");

if(themeToggle){

    themeToggle.addEventListener("click", function(){

        document.body.classList.toggle("dark-mode");

        if(document.body.classList.contains("dark-mode")){

            localStorage.setItem("theme","dark");

            themeToggle.innerHTML="☀️";

        }

        else{

            localStorage.setItem("theme","light");

            themeToggle.innerHTML="🌙";

        }

    });

}


window.onload=function(){

    if(localStorage.getItem("theme")=="dark"){

        document.body.classList.add("dark-mode");

        if(themeToggle){

            themeToggle.innerHTML="☀️";

        }

    }

};


/* =====================================
   Loading Spinner
===================================== */

const form=document.getElementById("resumeForm");

if(form){

form.addEventListener("submit",function(e){


const resume=document.getElementById("resume").value.trim();

const file=document.getElementById("resumeUpload").files.length;


// Allow textarea OR file upload

if(resume==="" && file===0){

alert("Please paste your resume or upload a PDF/TXT file.");

e.preventDefault();

return;

}


const loading=document.getElementById("loading");


if(loading){

loading.style.display="flex";

}


});

}

/* =====================================
   Upload TXT Resume
===================================== */

const upload=document.getElementById("resumeUpload");


if(upload){


upload.addEventListener("change",function(){


const file=this.files[0];


if(!file){

return;

}


// Check PDF or TXT

const filename=file.name.toLowerCase();


if(!filename.endsWith(".txt") && !filename.endsWith(".pdf")){


alert("Please upload only PDF or TXT files.");

this.value="";

return;

}



// Read only TXT files into textarea

if(filename.endsWith(".txt")){


const reader=new FileReader();


reader.onload=function(e){


document.getElementById("resume").value=e.target.result;


}


reader.readAsText(file);


}


// PDF will be handled by Flask


else if(filename.endsWith(".pdf")){


document.getElementById("resume").value =
"PDF Resume Uploaded: " + file.name;


}


});


}


/* =====================================
   Copy Result
===================================== */

function copyResult(){

let text="";

const category=document.querySelector("h2.text-success");

if(category){

text+="Predicted Category : "+category.innerText+"\n\n";

}

navigator.clipboard.writeText(text);

alert("Result copied successfully.");

}


/* =====================================
   Scroll Animation
===================================== */

window.addEventListener("scroll",function(){

const cards=document.querySelectorAll(".feature-card,.job-card,.glass-card");

cards.forEach(function(card){

const position=card.getBoundingClientRect().top;

const screen=window.innerHeight;

if(position<screen-100){

card.style.opacity="1";

card.style.transform="translateY(0px)";

}

});

});


/* =====================================
   Button Hover Effect
===================================== */

const buttons=document.querySelectorAll(".btn");

buttons.forEach(function(btn){

btn.addEventListener("mouseenter",function(){

btn.style.transform="translateY(-3px)";

});

btn.addEventListener("mouseleave",function(){

btn.style.transform="translateY(0px)";

});

});


/* =====================================
   Auto Hide Alerts
===================================== */

setTimeout(function(){

const alert=document.querySelector(".alert");

if(alert){

alert.style.display="none";

}

},5000);