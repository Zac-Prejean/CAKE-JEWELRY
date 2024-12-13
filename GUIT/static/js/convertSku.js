// convertSku.js    
    
export function convertSku(originalSku) { 
    const FRYDNMG2 = /FRYDNM-NKL-GLD-2N/i;
    const FRYDNMG3 = /FRYDNM-NKL-GLD-3N/i;
    const FRYDNMG4 = /FRYDNM-NKL-GLD-4N/i;
    const FRYDNMS2 = /FRYDNM-NKL-SLV-2N/i;
    const FRYDNMS3 = /FRYDNM-NKL-SLV-3N/i;
    const FRYDNMS4 = /FRYDNM-NKL-SLV-4N/i;
    const FRYDNMR2 = /FRYDNM-NKL-RSE-2N/i;
    const FRYDNMR3 = /FRYDNM-NKL-RSE-3N/i;
    const FRYDNMR4 = /FRYDNM-NKL-RSE-4N/i;
    const FRY4NM = /FRY4NM-NKL-RSE-4N/i;
    
    const DNR18 = /dnr-18kvermeil-small_personalized/i;

    let match; 
     
    if (originalSku.match(FRYDNMG2)) {    
        match = originalSku.match(FRYDNMG2);  
        return `NCK02GLDCHN01`;
    }
      
    if (originalSku.match(FRYDNMG3)) {    
        match = originalSku.match(FRYDNMG3);  
        return `NCK03GLDCHN01`;
    }

    if (originalSku.match(FRYDNMG4)) {    
        match = originalSku.match(FRYDNMG4);  
        return `NCK04GLDCHN01`;
    }

    if (originalSku.match(FRYDNMS2)) {    
        match = originalSku.match(FRYDNMS2);  
        return `NCK02SILCHN01`;
    }

    if (originalSku.match(FRYDNMS3)) {    
        match = originalSku.match(FRYDNMS3);  
        return `NCK03SILCHN01`;
    }

    if (originalSku.match(FRYDNMS4)) {    
        match = originalSku.match(FRYDNMS4);  
        return `NCK04SILCHN01`;
    }

    if (originalSku.match(FRYDNMR2)) {    
        match = originalSku.match(FRYDNMR2);  
        return `NCK02RSGCHN01`;
    }

    if (originalSku.match(FRYDNMR3)) {    
        match = originalSku.match(FRYDNMR3);  
        return `NCK03RSGCHN01`;
    }

    if (originalSku.match(FRYDNMR4)) {    
        match = originalSku.match(FRYDNMR4);  
        return `NCK04RSGCHN01`;
    }

    if (originalSku.match(FRY4NM)) {    
        match = originalSku.match(FRY4NM);  
        return `NCK04RSGCHN01`;
    }

    if (originalSku.match(DNR18)) {    
        match = originalSku.match(DNR18);  
        return `RNG46GLD`;
    }

    return originalSku;      
}