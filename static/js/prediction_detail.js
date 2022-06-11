// matrix cells

const cells = document.querySelectorAll('.cell');
const homeGoalsScored = document.querySelector('#script__goals-home');
const awayGoalsScored = document.querySelector('#script__goals-away');


function insertCellProbability() {
    cells.forEach((cell) => {
        let id = cell.id;
        let homeGoals = id.split('-')[0];
        let awayGoals = id.split('-')[1];
        let homeProb = document.querySelector(`#prob_hg_${homeGoals}`).innerHTML.slice(0, -1);
        let awayProb = document.querySelector(`#prob_ag_${awayGoals}`).innerHTML.slice(0, -1);
        homeProb = parseFloat(homeProb);
        awayProb = parseFloat(awayProb);
        let prob = homeProb * awayProb / 100;
        let p = document.createElement('p');
        p.innerHTML = `${prob.toFixed(2)}`;
        p.classList.add('cell__probability');
        if (homeGoalsScored.getAttribute('data') == homeGoals && awayGoalsScored.getAttribute('data') === awayGoals) {
            p.classList.add('cell__probability--highlighted');
        }        
        cell.appendChild(p);
    });
}

document.addEventListener('DOMContentLoaded', insertCellProbability);


function shadeCells() {
    cells.forEach((cell) => {
        let id = cell.id;
        let homeGoals = id.split('-')[0];
        let awayGoals = id.split('-')[1];
        let homeProb = document.querySelector(`#prob_hg_${homeGoals}`).innerHTML.slice(0, -1);
        let awayProb = document.querySelector(`#prob_ag_${awayGoals}`).innerHTML.slice(0, -1);
        homeProb = parseFloat(homeProb);
        awayProb = parseFloat(awayProb);
        let alphaValue = (homeProb * awayProb) / 1000;
        if (alphaValue > 1) {
            alphaValue = 1;
        }
        let color = `rgba(6, 177, 120, ${alphaValue})`;
        cell.style.backgroundColor = color;
    });
}

document.addEventListener('DOMContentLoaded', shadeCells);


// move navigation section for desktop

// 800px

const navigationSection = document.querySelector('#navigation');
const defaultParentNav = navigationSection.parentElement;
const desktopParent = document.querySelector('#desktop-left')

function moveNavigation() {
    if (window.innerWidth >= 800) {
        desktopParent.appendChild(navigationSection);
    }
    else {
        defaultParentNav.appendChild(navigationSection);
    }
    console.log(window.innerWidth)
}

document.addEventListener('DOMContentLoaded', moveNavigation);
window.addEventListener('resize', moveNavigation);