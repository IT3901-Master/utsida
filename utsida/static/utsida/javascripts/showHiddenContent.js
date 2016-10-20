var acc = document.getElementsByClassName("accordion");

for (var i = 0; i < acc.length; i++) {
    acc[i].onclick = function() {
        this.classList.toggle("active");
        this.previousElementSibling.classList.toggle("show");
        if (this.firstChild.innerHTML === "Vis ekstra informasjon") {
            this.firstChild.innerHTML = "Skjul ekstra informasjon";
        }
        else if (this.firstChild.innerHTML === "Skjul ekstra informasjon"){
            this.firstChild.innerHTML = "Vis ekstra informasjon";
        }
    }
}