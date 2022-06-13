// resize elements in hero banner for responsive design

const heroHeading = document.querySelector('.hero__heading')
const heroText = document.querySelector('#hero__text')

function setHeroMargins(){
    let margin = heroHeading.offsetHeight / 1.5
    let marginBig = margin * 2
    if (margin < 16) {
        margin = 16
    }
    heroHeading.style.margin = `${margin}px 0`;
    heroText.style.margin = `${margin}px 0`;
    console.log(margin)
}

document.addEventListener('DOMContentLoaded', setHeroMargins)
window.addEventListener('resize', setHeroMargins)



// move buttons for responsive design

const predBtn = document.querySelector('#pred-btn')
const defaultParentPred = predBtn.parentElement
const desktopParentPred = document.querySelector('#data-text')
const analysisBtn = document.querySelector('#analysis-btn')
const defaultParentAnalysis = analysisBtn.parentElement
const desktopParentAnalysis = document.querySelector('#predictions-text')

function movePredBtn(){
    if (window.innerWidth >= 900) {
        desktopParentPred.appendChild(predBtn)
        desktopParentAnalysis.appendChild(analysisBtn)
    }
    else {
        defaultParentPred.appendChild(predBtn)
        defaultParentAnalysis.appendChild(analysisBtn)
    }
}

document.addEventListener('DOMContentLoaded', movePredBtn)
window.addEventListener('resize', movePredBtn)