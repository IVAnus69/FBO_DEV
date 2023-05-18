
//var upward = document.querySelector('.upward');
function scrollToTop(){
	window.scrollTo(0, 0);
}

window.addEventListener('scroll', function(){
	if(window.scrollY > 1){
		document.querySelector('.upward').classList.add('active')
	}
	else {
		document.querySelector('.upward').classList.remove('active')
	}
})