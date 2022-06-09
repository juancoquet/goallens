// matrix cells

const cells = document.querySelectorAll('.cell');


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