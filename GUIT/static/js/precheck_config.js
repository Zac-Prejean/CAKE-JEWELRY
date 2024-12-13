// precheck_config.js

// RINGS
const prefixRNG = "RNG";
const oneLineRNG = [

];

const twoLineRNG = [

"35GLD", "35SIL", "35RSG", "46GLD", "46SIL", "46RSG", "68GLD", "68SIL", "68RSG", "78GLD", "78SIL", "78RSG",
"910GLD", "911SIL", "910RSG", "911GLD", "911SIL", "911RSG", 
"DBL35GLD", "DBL35SIL", "DBL35RSG", "DBL46GLD", "DBL46SIL", "DBL46RSG", "DBL68GLD", "DBL68SIL", "DBL68RSG", 
"DBL78GLD", "DBL78SIL", "DBL78RSG", "DBL910GLD", "DBL910SIL", "DBL910RSG", "DBL911GLD", "DBL911SIL", "DBL911RSG",
];

const validSkus_1ring = oneLineRNG.map(suffix => prefixRNG + suffix);
const validSkus_2ring = twoLineRNG.map(suffix => prefixRNG + suffix);

// NECKLESS
const prefixNCK = "NCK";
const oneLineNck = [

"GLDCHN01", "SILCHN01", "RSGCHN01", "BFLGLDCHN01", "BFLSILCHN01", "BFLRSGCHN01", "GLDCHN01PSCVT", "SILCHN01PSCVT", "RSGCHN01PSCVT",
"GLDCHN01JMQF", "SILCHN01JMQF", "RSGCHN01JMQF", "GLDCHN01JMMF", "SILCHN01JMMF", "RSGCHN01JMMF", "GLDCHN01JMAF", "SILCHN01JMAF", "RSGCHN01JMAF", 
"GLDCHN01JMDF", "SILCHN01JMDF", "RSGCHN01JMDF"]

const twoLineNck = [

"02GLDCHN01", "02SILCHN01", "02RSGCHN01"];

const threeLineNck = [

"03GLDCHN01", "03SILCHN01", "03RSGCHN01", "FRYDNM-NKL-GLD-3N", "FRYDNM-NKL-SLV-3N", "FRYDNM-NKL-RSE-3N"];

const fourLineNck = [

"04GLDCHN01", "04SILCHN01", "04RSGCHN01", "FRYDNM-NKL-GLD-4N", "FRYDNM-NKL-SLV-4N", "FRYDNM-NKL-RSE-4N"];

const validSkus_1neckless = oneLineNck.map(suffix => prefixNCK + suffix);
const validSkus_2neckless = twoLineNck.map(suffix => prefixNCK + suffix);
const validSkus_3neckless = threeLineNck.map(suffix => prefixNCK + suffix);
const validSkus_4neckless = fourLineNck.map(suffix => prefixNCK + suffix);

// NECKLESS
const prefixFRY = "FRY";

const twoLineFry = [

"DNM-NKL-GLD-2N", "DNM-NKL-SLV-2N", "DNM-NKL-RSE-2N"];

const threeLineFry = [

"DNM-NKL-GLD-3N", "DNM-NKL-SLV-3N", "DNM-NKL-RSE-3N"];

const fourLineFry = [

"DNM-NKL-GLD-4N", "DNM-NKL-SLV-4N", "DNM-NKL-RSE-4N"];

const validSkus_2fryneckless = twoLineFry.map(suffix => prefixFRY + suffix);
const validSkus_3fryneckless = threeLineFry.map(suffix => prefixFRY + suffix);
const validSkus_4fryneckless = fourLineFry.map(suffix => prefixFRY + suffix);


export function applyFontRule(originalOptions) {      
    let newOptions = originalOptions; 
    
        // Replace "Custom Name Top:" and "Custom Name Bottom:" with "Personalization:"  
        const customNameTopMatch = newOptions.match(/Custom Name Top:\s*([^,]*)/);  
        const customNameBottomMatch = newOptions.match(/Custom Name Bottom:\s*([^,]*)/);  
      
        if (customNameTopMatch && customNameBottomMatch) {  
            const customNameTop = customNameTopMatch[1].trim();  
            const customNameBottom = customNameBottomMatch[1].trim();  
            newOptions = newOptions.replace(/Custom Name Top:\s*([^,]*),?\s*/, '');  
            newOptions = newOptions.replace(/Custom Name Bottom:\s*([^,]*),?\s*/, '');  
            newOptions = `Personalization:${customNameTop}${customNameBottom}`;  
        }  
  
    const fontMatch = originalOptions.match(/(font:)([^,]*)(,|$)/);      
    const fontValue = fontMatch ? fontMatch[2].trim() : "Nella Sue";  
    
    let nameKeywords = ['Name 1:', 'Name 2:', 'Name 3:', 'Name 4:'];    
    let nameValues = [];    
    
    for (const keyword of nameKeywords) {    
        const nameMatch = newOptions.match(new RegExp(`(${keyword})([^,]*)(,|$)`));    
        if (nameMatch) {    
            nameValues.push(nameMatch[2].trim());    
            newOptions = newOptions.replace(new RegExp(`(${keyword})([^,]*)(,|$)`), '');    
        }    
    }  
    
    // conversion from csv to uppdated csv
    if (fontMatch) {    
        newOptions = newOptions.replace(/(Custom Name Top:)([^,]*)(,|$)/, `$1$2, font: ${fontValue}$3`);    
        newOptions = newOptions.replace(/(Custom Name Bottom:)([^,]*)(,|$)/, `$1$2, font: ${fontValue}$3`);    
        newOptions = newOptions.replace(/(,\s*font:)([^,]*)(,|$)/, '');    
    }  
  
    if (nameValues.length > 0) {    
        newOptions = newOptions.replace(/Personalization:(.*?)(,|$)/s, `Personalization:"${nameValues.join('\n')}"$2`);   
    }      
      
    if (originalOptions.includes('font: Al Libretto')) {  
        newOptions = newOptions.replace(/,\s*font:\s*Al Libretto/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Al Libretto, Personalization:');  
    } else if (originalOptions.includes('font: Autumn Chant')) {  
        newOptions = newOptions.replace(/,\s*font:\s*Autumn Chant/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Mon Amour, Personalization:');  
    } else if (originalOptions.includes('_fulfillment:Font: Autumn Chant')) {  
        newOptions = newOptions.replace(/_fulfillment:Font:\s*Autumn Chant/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Mon Amour Months, Personalization:'); 
    } else if (originalOptions.includes('font: Shelby Bold')) {  
        newOptions = newOptions.replace(/,\s*font:\s*Shelby Bold/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Bella, Personalization:');   
    } else if (originalOptions.includes('font: Bella')) {  
        newOptions = newOptions.replace(/,\s*font:\s*Bella/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Bella, Personalization:');  
    } else if (originalOptions.includes('font: Buffalo Nickel')) {  
        newOptions = newOptions.replace(/,\s*font:\s*Buffalo Nickel/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Buffalo Nickel, Personalization:');
    } else if (originalOptions.includes('font: Cervantiss')) {  
        newOptions = newOptions.replace(/,\s*font:\s* Cervantiss/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Cervanttis, Personalization:');  
    } else if (originalOptions.includes('font: Cervanttis')) {  
        newOptions = newOptions.replace(/,\s*font:\s*Cervanttis/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Cervanttis, Personalization:');  
    } else if (originalOptions.includes('font: Claster Regular')) {  
        newOptions = newOptions.replace(/,\s*font:\s*Claster Regular/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Claster Regular, Personalization:'); 
    } else if (originalOptions.includes('font: Fairwater Script Regular')) {  
        newOptions = newOptions.replace(/,\s*font:\s*Fairwater Script Regular/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Fairwater, Personalization:'); 
    } else if (originalOptions.includes('font: Nella Sue')) {  
        newOptions = newOptions.replace(/,\s*font:\s*Nella Sue/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: Fairy-Bold, Personalization:');
    } else if (originalOptions.includes('font: UKIJ')) {  
        newOptions = newOptions.replace(/,\s*font:\s*UKIJ/, '');  
        newOptions = newOptions.replace(/Custom Name:/, 'Design: UKIJ, Personalization:');  
    } else if (originalOptions.includes('Custom Name:')) {  
        newOptions = newOptions.replace(/(Custom Name:)([^,]*)(,|$)/, `Design: Default, Personalization:$2$3`);  
    } 
     
        const name1Match = originalOptions.match(/(Name 1:)([^,]*)(,|$)/);  
        const name2Match = originalOptions.match(/(Name 2:)([^,]*)(,|$)/);  
        const name3Match = originalOptions.match(/(Name 3:)([^,]*)(,|$)/); 
        const name4Match = originalOptions.match(/(Name 4:)([^,]*)(,|$)/); 
        const middleinscriptionMatch = originalOptions.match(/(Middle Inscription:)([^,]*)(,|$)/);
        const leftInscriptionMatch = originalOptions.match(/(Left Inscription:)([^,]*)(,|$)/);  
        const rightInscriptionMatch = originalOptions.match(/(Right Inscription:)([^,]*)(,|$)/);
        const outsidenameMatch = originalOptions.match(/(Outside Inscription:)([^,]*)(,|$)/);  
        const insidenameMatch = originalOptions.match(/(Inside Inscription:)([^,]*)(,|$)/); 
      
        // names 
        if (name1Match && name2Match && name3Match && name4Match) {      
            newOptions = originalOptions.replace(/(Name 1:)([^,]*)(,|$)/, `Design: ${fontValue}, Personalization:${name1Match[2].trim()}\n${name2Match[2].trim()}$3\n${name3Match[2].trim()}$3\n${name4Match[2].trim()}$3`);      
            newOptions = newOptions.replace(/(Name 2:)([^,]*)(,|$)/, '');      
            newOptions = newOptions.replace(/(Name 3:)([^,]*)(,|$)/, '');
            newOptions = newOptions.replace(/(Name 4:)([^,]*)(,|$)/, '');
        } else if (name1Match && name2Match && name3Match) {      
            newOptions = originalOptions.replace(/(Name 1:)([^,]*)(,|$)/, `Design: ${fontValue}, Personalization:${name1Match[2].trim()}\n${name2Match[2].trim()}$3\n${name3Match[2].trim()}$3`);      
            newOptions = newOptions.replace(/(Name 2:)([^,]*)(,|$)/, '');      
            newOptions = newOptions.replace(/(Name 3:)([^,]*)(,|$)/, '');      
        } else if (name1Match && name2Match) {  
            newOptions = originalOptions.replace(/(Name 1:)([^,]*)(,|$)/, `Design: ${fontValue}, Personalization:${name1Match[2].trim()}\n${name2Match[2].trim()}$3`);  
            newOptions = newOptions.replace(/(Name 2:)([^,]*)(,|$)/, '');  
        } else if (name1Match) {  
            newOptions = originalOptions.replace(/(Name 1:)([^,]*)(,|$)/, `Design: ${fontValue}, Personalization:${name1Match[2].trim()}$3`);  
        // inscriptions
        } else if (leftInscriptionMatch && middleinscriptionMatch && rightInscriptionMatch) {        
            newOptions = originalOptions.replace(/(Left Inscription:)([^,]*)(,|$)/, `Design: ${fontValue}, Personalization:${leftInscriptionMatch[2].trim()}\n${middleinscriptionMatch[2].trim()}$3\n${rightInscriptionMatch[2].trim()}$3`);        
            newOptions = newOptions.replace(/(Middle Inscription:)([^,]*)(,|$)/, ''); 
            newOptions = newOptions.replace(/(Right Inscription:)([^,]*)(,|$)/, '');   
        } else if (leftInscriptionMatch && rightInscriptionMatch) {  
            newOptions = originalOptions.replace(/(Left Inscription:)([^,]*)(,|$)/, `Design: ${fontValue}, Personalization:${leftInscriptionMatch[2].trim()}\n${rightInscriptionMatch[2].trim()}$3`);  
            newOptions = newOptions.replace(/(Right Inscription:)([^,]*)(,|$)/, '');  
        }  
        if (fontMatch) {  
            newOptions = newOptions.replace(/(,\s*font:)([^,]*)(,|$)/, '');  
        }  
        
        newOptions = newOptions.replace(/,\s*$/, '');  

        console.log("New Options:", newOptions);  
        return newOptions;  
    }

export { prefixNCK, prefixRNG, oneLineNck, twoLineNck, threeLineNck, fourLineNck, twoLineFry, threeLineFry, fourLineFry, oneLineRNG, twoLineRNG};  
    
export const validSkus = [ ...validSkus_1neckless, ...validSkus_2neckless, ...validSkus_3neckless, ...validSkus_4neckless, ...validSkus_2fryneckless, ...validSkus_3fryneckless, ...validSkus_4fryneckless, ...validSkus_1ring, ...validSkus_2ring];
