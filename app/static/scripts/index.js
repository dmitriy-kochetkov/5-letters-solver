const WORD_SEND_URL = '/word'
const CALC_VARS_URL = '/calc_variants'

let determinedLetters = {}
let letterLeaveTimer
let letterPopup

function removeStatusClassnames(target) {
    target.classList.remove('excluded')
    target.classList.remove('included')
    target.classList.remove('undefined')
    target.classList.remove('determined')
}

function setLetterClassname(target) {
    let id = parseInt(target.id.split('-')[1])
    let letter = target.innerText

    if (letter) {
        if ( determinedLetters[id] === letter ) {
            removeStatusClassnames(target)
            target.classList.add('determined')
            target.removeEventListener("mouseover", undefinedLetterMouseHover)
            target.removeEventListener("mouseout", undefinedLetterMouseOut)
        } else {
            removeStatusClassnames(target)
            target.classList.add('undefined')
            target.addEventListener("mouseover", undefinedLetterMouseHover)
            target.addEventListener("mouseout", undefinedLetterMouseOut)
        }
    } else {
        removeStatusClassnames(target)
        target.classList.add('excluded')
        target.removeEventListener("mouseover", undefinedLetterMouseHover)
        target.removeEventListener("mouseout", undefinedLetterMouseOut)
    }
}

function updateSendButtonState() {
    if (isAllLettersConfigured()) {
        enadleSendButton()
    } else {
        disableSendButton()
    }
}

function hideEmpyWordsBanner() {
    let banner = document.querySelector('#no-words-banner')
    banner.style.display = 'none'
}

function showEmpyWordsBanner() {
    let banner = document.querySelector('#no-words-banner')
    banner.style.display = 'block'
}

function isPopupVisible() {
    let popup = document.querySelector('#popup-0')
    return popup.style.display != 'none'
}

function hidePopup() {
    let popup = document.querySelector('#popup-0')
    popup.style.display = 'none'
}

function isAllLettersConfigured() {
    for (i=0; i<5; i++) {
        let input = document.querySelector('#input-'+i)
        let letter = input.innerText
        if (!letter || input.classList.value.includes('undefined')) {
            return false
        }
    }
    return true
}

function changeLetterTypeHandler(event) {
    if (letterPopup) {
        removeStatusClassnames(letterPopup)
        letterPopup.classList.add(event.target.value)
    }   
    updateSendButtonState()
}

function undefinedLetterMouseHover(event) {
    targetBCR = event.target.getBoundingClientRect()            

    let popup = document.querySelector('#popup-0')
    popup.style.display = 'flex';
    popup.style.position = 'absolute'
    popup.style.top = `${targetBCR.bottom + 5}px`
    popup.style.left = `${targetBCR.left}px`

    letterPopup = event.target

    // init popup

    children = popup.children
    for (i=0; i<children.length; i++) {
        if (letterPopup.classList.value.includes(children[i].value)) {
            children[i].checked = true;
        } else {
            children[i].checked = false;
        }
    }

    if (letterLeaveTimer){
        clearTimeout(letterLeaveTimer)
    }
}

function undefinedLetterMouseOut(event) {
    letterLeaveTimer = setTimeout(function () {
        let popup = document.querySelector('#popup-0')
        popup.style.display = 'none'
    }, 300);
}

function popupMouseEnter(event) {
    if (letterLeaveTimer){
        clearTimeout(letterLeaveTimer)
    }
}

function popupMouseLeave(event) {
    letterLeaveTimer = setTimeout(function () {
        let popup = document.querySelector('#popup-0')
        popup.style.display = 'none'
    }, 300);
}

function inputHandler(event) {
    let text = event.target.innerText.toUpperCase().replace(/\s+/g, '');
    event.target.innerText = text
    let id = parseInt(event.target.id.split('-')[1])
    inputs = findInputs()

    if (!text) {
        //Пустое поле (Backspace)
        // Скрываем popup если он активен для текущией буквы
        if (letterPopup && letterPopup == event.target && isPopupVisible()) {
            hidePopup()
        }

        if (id > 0) {
            setCaret(inputs[id-1])
        }
    } else if (text.length === 1) {
        // 1 символ
        if (id < 4) {
            setCaret(inputs[id+1])
        } else {
            setCaret(event.target)
        }
    } else {
        // строка
        text = text.slice(0, 5-id)
        pos = id

        for (i=0; i<text.length; i++) {
            pos = id + i;
            inputs[pos].innerText = text[i]
            setLetterClassname(inputs[pos])
        }
        setCaret(inputs[pos])
    }

    setLetterClassname(event.target)
    updateSendButtonState()
}

function keydownHandler(event) {
    let id = parseInt(event.target.id.split('-')[1])
    inputs = findInputs()

    if (!event.target.innerText && event.key === "Backspace") {
        if (id > 0) {
            setLetterClassname(event.target)
            setCaret(inputs[id-1])
        }
    }
}

function findInputs(){
    let inputs = []
    for (i=0; i<5; i++) {
        let input = document.querySelector('#input-'+i)
        inputs.push(input)
    }
    return inputs
}

function setCaret(element) {
    var range = document.createRange()
    var sel = window.getSelection()

    len = element.innerText.length
    range.setStart(element, len)
    range.collapse(true)
    
    sel.removeAllRanges()
    sel.addRange(range)
}

function enadleSendButton() {
    let btn = document.querySelector('#send-word-btn')
    if (btn) {
        btn.disabled = false
    }
}

function disableSendButton() {
    let btn = document.querySelector('#send-word-btn')
    if (btn) {
        btn.disabled = true
    }
}

function getWord() {
    letters = []
    for (i=0; i<5; i++) {
        let input = document.querySelector('#input-'+i)
        letters.push(input.innerText)
    }
    return letters.join('')
}

function getMaskString() {
    mask = []
    for (i=0; i<5; i++) {
        let input = document.querySelector('#input-'+i)
        if (input.classList.value.includes('included')) {
            mask.push('^')
        } else if (input.classList.value.includes('excluded')) {
            mask.push('.')
        } else if (input.classList.value.includes('determined')) {
            mask.push('!')
        }
    }
    return mask.join('')
}

function convertMaskSymbolToClassname(symbol) {
    let result = 'excluded'
    switch(symbol) {
        case '^':
            result = 'included'
            break;
        case '!':
            result = 'determined'
            break
    }
    return result
}

function сreateAndShowNewWord(word_json) {
    wordsContainer = document.querySelector("#words-container")
    wrapperDiv = document.createElement('div')
    wrapperDiv.classList.add('word')

    for (i=0; i<word_json.body.length; i++) {
        letter = word_json.body[i]
        maskSymbol = word_json.mask[i]

        letterDiv = document.createElement('div')
        letterDiv.classList.add('letter')
        letterDiv.classList.add('big-letter')
        letterDiv.classList.add(convertMaskSymbolToClassname(maskSymbol))
        letterDiv.innerText = letter

        wrapperDiv.appendChild(letterDiv)
    }

    if (wordsContainer) {
        wordsContainer.appendChild(wrapperDiv)
    }
}

async function sendButtonClick() {
    const word = getWord()
    const mask = getMaskString()
    const data = { "body": word, "mask": mask };
    //console.log(data)

    try {
        const response = await fetch(WORD_SEND_URL, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
            'Content-Type': 'application/json'
            }
        });
        const json = await response.json();
        сreateAndShowNewWord(json)
        hideEmpyWordsBanner()
        resetAllInputs()
        updateDeterminedLetters()
        updateVariants()
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function updateVariants() {
    try {
        const response = await fetch(CALC_VARS_URL, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json'
            }
        });
        const json = await response.json();

        if (json.total) {
            setTotalVariatsCount(json.total)
        }
        if (json.words) {
            setVartiants(json.words)
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

function setTotalVariatsCount(count) {
    counterSpan = document.querySelector("#total-variants-count")
    counterSpan.innerText = count
}

function setVartiants(variants) {
    variantsContainer = document.querySelector("#variants-container")
    variantsContainer.innerHTML = ''

    for (key in variants) {
        variantDiv = document.createElement('div')
        variantDiv.classList.add('variant-item')
        variantDiv.innerText = variants[key].toLowerCase()

        variantsContainer.appendChild(variantDiv)
    }    
}

function resetAllInputs() {
    for (i=0; i<5; i++) {
        let input = document.querySelector('#input-'+i)
        input.innerText = ''
        setLetterClassname(input)
    }
    updateSendButtonState()
}

// Обновление словаря с установленными буквам. Проверка проводится на фронте на основании уже отображенных слов.
function updateDeterminedLetters() {
    wordsContainer = document.querySelector("#words-container")
    words = wordsContainer.children

    for (i=0; i<words.length; i++) {
        letters = words[i].children

        for(j=0; j<letters.length; j++) {
            if (letters[j].classList.value.includes("determined")) {
                determinedLetters[j] = letters[j].innerText
            }
        }
    }
}

function setLettersToInputs(word) {
    if (word.length != 5) {
        return
    }
    inputs = findInputs()
    for (i=0; i<inputs.length; i++) {
        inputs[i].innerText = word[i].toUpperCase()
        setLetterClassname(inputs[i])
    }
}

// Обработчик клика по варианту возможного слова
function variantClick(event) {   
    if (event.target.classList.value.includes("variant-item")) {
        setLettersToInputs(event.target.innerText)
    }
}

function initAll() {
    updateDeterminedLetters()
}

document.addEventListener('DOMContentLoaded',initAll);
