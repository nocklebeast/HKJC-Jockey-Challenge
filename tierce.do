
cd M:\python\hkjc\odds_files
import delimited "TierceInvestments11.csv", delimiter(comma)   case(preserve)  clear

//egen Total1 = sum(TINV1)
//gen T1 = TINV1 / Total1

gen Race = 11
drop TINV*
sort Race horseno
save TierceInvestments.dta, replace

//rename horseno xHorseno

foreach var in horseno T1Ch T2Ch T3Ch {
    rename `var' x`var'
}

save xTierce.dta, replace

foreach var in horseno T1Ch T2Ch T3Ch {
    rename x`var' y`var'
}
save yTierce.dta, replace


foreach var in horseno T1Ch T2Ch T3Ch {
    rename y`var' z`var'
}
save zTierce.dta, replace 


use xTierce.dta, clear
sort Race xhorseno
joinby Race using  yTierce.dta 
sort Race xhorseno yhorseno
drop if xhorseno == yhorseno
order Race xhorseno yhorseno
sort Race xhorseno yhorseno
save xyTierce.dta, replace

joinby Race  using zTierce.dta
sort Race xhorseno yhorseno zhorseno
order Race xhorseno yhorseno zhorseno
drop if xhorseno == zhorseno 
drop if yhorseno == zhorseno

// the original "bayes/conditional probability" in the old hk betting app.
//gen TCh = xT1Ch * yT2Ch * zT3Ch / (1-xT2Ch) / (1-xT3Ch-yT3Ch) 
// boxed trifectas?
//XYZ
gen TXYZ123 = xT1Ch * yT2Ch * zT3Ch / (1-xT2Ch) / (1-xT3Ch-yT3Ch) 
gen TXYZ132 = xT1Ch * yT3Ch * zT2Ch / (1-xT3Ch) / (1-xT2Ch-yT2Ch) 
//XYZ
gen TXYZ213 = xT2Ch * yT1Ch * zT3Ch / (1-xT1Ch) / (1-xT3Ch-yT3Ch) 
gen TXYZ231 = xT2Ch * yT3Ch * zT1Ch / (1-xT3Ch) / (1-xT1Ch-yT1Ch) 
//XYZ
gen TXYZ312 = xT3Ch * yT1Ch * zT2Ch / (1-xT1Ch) / (1-xT2Ch-yT2Ch) 
gen TXYZ321 = xT3Ch * yT2Ch * zT1Ch / (1-xT2Ch) / (1-xT1Ch-yT1Ch) 

//XZY
gen TXZY123 = xT1Ch * zT2Ch * yT3Ch / (1-xT2Ch) / (1-xT3Ch-zT3Ch) 
gen TXZY132 = xT1Ch * zT3Ch * yT2Ch / (1-xT3Ch) / (1-xT2Ch-zT2Ch) 
//XZY
gen TXZY213 = xT2Ch * zT1Ch * yT3Ch / (1-xT1Ch) / (1-xT3Ch-zT3Ch) 
gen TXZY231 = xT2Ch * zT3Ch * yT1Ch / (1-xT3Ch) / (1-xT1Ch-zT1Ch) 
//XZY
gen TXZY312 = xT3Ch * zT1Ch * yT2Ch / (1-xT1Ch) / (1-xT2Ch-zT2Ch) 
gen TXZY321 = xT3Ch * zT2Ch * yT1Ch / (1-xT2Ch) / (1-xT1Ch-zT1Ch) 
/////////////////
//YXZ
gen TYXZ123 = yT1Ch * xT2Ch * zT3Ch / (1-yT2Ch) / (1-yT3Ch-xT3Ch) 
gen TYXZ132 = yT1Ch * xT3Ch * zT2Ch / (1-yT3Ch) / (1-yT2Ch-xT2Ch) 
//YXZ
gen TYXZ213 = yT2Ch * xT1Ch * zT3Ch / (1-yT1Ch) / (1-yT3Ch-xT3Ch)   // 123 23
gen TYXZ231 = yT2Ch * xT3Ch * zT1Ch / (1-yT3Ch) / (1-yT1Ch-xT1Ch) 	//
//YXZ
gen TYXZ312 = yT3Ch * xT1Ch * zT2Ch / (1-yT1Ch) / (1-yT2Ch-xT2Ch)   //xyz xxy
gen TYXZ321 = yT3Ch * xT2Ch * zT1Ch / (1-yT2Ch) / (1-yT1Ch-xT1Ch)  
/////////////////////
//YZX
gen TYZX123 = yT1Ch * zT2Ch * xT3Ch / (1-yT2Ch) / (1-yT3Ch-zT3Ch) 
gen TYZX132 = yT1Ch * zT3Ch * xT2Ch / (1-yT3Ch) / (1-yT2Ch-zT2Ch) 
//YXZ
gen TYZX213 = yT2Ch * zT1Ch * xT3Ch / (1-yT1Ch) / (1-yT3Ch-zT3Ch) 
gen TYZX231 = yT2Ch * zT3Ch * xT1Ch / (1-yT3Ch) / (1-yT1Ch-zT1Ch) 
//YXZ
gen TYZX312 = yT3Ch * zT1Ch * xT2Ch / (1-yT1Ch) / (1-yT2Ch-zT2Ch) 
gen TYZX321 = yT3Ch * zT2Ch * xT1Ch / (1-yT2Ch) / (1-yT1Ch-zT1Ch) 
///////////////////
//ZXY
gen TZXY123 = zT1Ch * xT2Ch * yT3Ch / (1-zT2Ch) / (1-zT3Ch-xT3Ch) 
gen TZXY132 = zT1Ch * xT3Ch * yT2Ch / (1-zT3Ch) / (1-zT2Ch-xT2Ch) 
//ZXY
gen TZXY213 = zT2Ch * xT1Ch * yT3Ch / (1-zT1Ch) / (1-zT3Ch-xT3Ch) 
gen TZXY231 = zT2Ch * xT3Ch * yT1Ch / (1-zT3Ch) / (1-zT1Ch-xT1Ch) 
//ZXY
gen TZXY312 = zT3Ch * xT1Ch * yT2Ch / (1-zT1Ch) / (1-zT2Ch-xT2Ch)  
gen TZXY321 = zT3Ch * xT2Ch * yT1Ch / (1-zT2Ch) / (1-zT1Ch-xT1Ch) 
////////////////////
//ZYX
gen TZYX123 = zT1Ch * yT2Ch * xT3Ch / (1-zT2Ch) / (1-zT3Ch-yT3Ch) 
gen TZYX132 = zT1Ch * yT3Ch * xT2Ch / (1-zT3Ch) / (1-zT2Ch-yT2Ch) 
//ZYX
gen TZYX213 = zT2Ch * yT1Ch * xT3Ch / (1-zT1Ch) / (1-zT3Ch-yT3Ch) 
gen TZYX231 = zT2Ch * yT3Ch * xT1Ch / (1-zT3Ch) / (1-zT1Ch-yT1Ch) 
//ZYX
gen TZYX312 = zT3Ch * yT1Ch * xT2Ch / (1-zT1Ch) / (1-zT2Ch-yT2Ch) 
gen TZYX321 = zT3Ch * yT2Ch * xT1Ch / (1-zT2Ch) / (1-zT1Ch-yT1Ch) 

gen TrioCh = 0
global L " XYZ XZY YXZ YZX ZXY ZYX "
global M " 123 132 213 231 312 321 "
foreach xxx of global L {
	foreach mmm of global M {
		egen tot`xxx'`mmm' = sum(T`xxx'`mmm'), by(Race)
		replace TrioCh = TrioCh + T`xxx'`mmm'
	}
}
replace TrioCh = TrioCh / 36
// all egen sum to 1
drop tot*
gen tot = 1

aorder
order Race xhorseno yhorseno zhorseno tot* TrioCh TX* TY* TZ*

browse

					
// collapses on xhorseno to get correct tierce investment on position 1
gen T1X = 0
replace T1X = T1X + TXYZ123 + TXYZ132 + TXZY123 + TXZY132 
replace T1X = T1X / 4	

// collapses on yhorseno to get correct tierce investment on position 2
gen T2Y = 0
replace T2Y = T2Y + TYXZ213 + TYXZ231 + TYZX213 + TYZX231 
replace T2Y = T2Y / 4	

// collapses on yhorseno to get correct tierce investment on position 3
gen T3Z = 0
replace T3Z = T3Z + TZXY312 + TZXY321 + TZYX312 + TZYX321
replace T3Z = T3Z / 4

//gen TiercePay = (1-0.25) / TierceCh

gen TierceCh = (T1X + T2Y + T3Z) / 3


corr TrioCh T* 

aorder
order Race xhorseno yhorseno zhorseno TrioCh TierceCh T*   
save xyzTierce.dta, replace
browse 
stop

//"TierceCh is different in the trio combinations (and normalized to 1)
/*
browse if (xhorseno == 1 & yhorseno == 2 & zhorseno ==3) ///
        | (xhorseno == 1 & yhorseno == 3 & zhorseno ==2) ///
		| (xhorseno == 2 & yhorseno == 1 & zhorseno ==3) ///
		| (xhorseno == 2 & yhorseno == 3 & zhorseno ==1) ///
		| (xhorseno == 3 & yhorseno == 1 & zhorseno ==2) ///
		| (xhorseno == 3 & yhorseno == 2 & zhorseno ==1)
		
*/

// T1 on x collapses to T1 investment chance
// T2* on y collapses to T2 investment chance
// T3* on z collapses on T3 investment chance.

use xyzTierce.dta, clear
collapse (sum) TrioCh TierceCh T1X T2Y T3Z TX* TY* TZ* , by(Race xhorseno)
browse if xhorseno == 1 

stop

use xyzTierce.dta, clear
collapse (sum) TrioCh TierceCh T1X T2Y T3Z TY* TX*  TZ*  , by(Race yhorseno)
//collapse (sum) TrioCh T1X T2Y T3Z  TX* TY* TZ*  , by(Race yhorseno)
browse if yhorseno == 1 | yhorseno == 2

use xyzTierce.dta, clear
collapse (sum) TrioCh TierceCh T1X T2Y T3Z TZ* TX* TY*   ,by(Race zhorseno)
browse if zhorseno == 1 | zhorseno == 2 | zhorseno == 3


browse


stop

/*
// for trio?
gen T6X = (T1X23 + T1X32 + T2X13 + T2X31 + T3X12 + T3X21) / 6
//or for trifecta?
gen T2X = (T1X23 + T1X32) / 2

//Y
gen T2Y13 = xT1Ch * yT2Ch * zT3Ch / (1-yT1Ch) / (1-yT3Ch-xT3Ch) //  2 and y
gen T2Y31 = xT3Ch * yT2Ch * zT1Ch / (1-yT3Ch) / (1-yT1Ch-xT1Ch) //  2 and y
//Y
gen T1Y23 = xT2Ch * yT1Ch * zT3Ch / (1-yT2Ch) / (1-yT3Ch-xT3Ch) //  2 and y
gen T1Y32 = xT3Ch * yT1Ch * zT2Ch / (1-yT3Ch) / (1-yT2Ch-xT2Ch) //  2 and y
//Y
gen T3Y12 = xT1Ch * yT3Ch * zT2Ch / (1-yT1Ch) / (1-yT2Ch-xT2Ch) //  2 and y
gen T3Y21 = xT2Ch * yT3Ch * zT1Ch / (1-yT2Ch) / (1-yT1Ch-xT1Ch) //  2 and y

gen T6Y = ( T2Y13 + T2Y31 + T1Y23 + T1Y32 + T3Y12 + T3Y21 ) / 6
gen T2Y = ( T2Y13 + T2Y31 ) / 2

//Z
gen T3Z12 = xT1Ch * yT2Ch * zT3Ch / (1-zT1Ch) / (1-zT2Ch-xT2Ch) //  3 and z
gen T3Z21 = xT2Ch * yT1Ch * zT3Ch / (1-zT2Ch) / (1-zT1Ch-xT1Ch) //  3 and z
//Z
gen T1Z32 = xT3Ch * yT2Ch * zT1Ch / (1-zT3Ch) / (1-zT2Ch-xT2Ch) //  3 and z
gen T1Z23 = xT2Ch * yT3Ch * zT1Ch / (1-zT2Ch) / (1-zT3Ch-xT3Ch) //  3 and z
//Z
gen T2Z13 = xT1Ch * yT3Ch * zT2Ch / (1-zT1Ch) / (1-zT3Ch-xT3Ch) //  3 and z
gen T2Z31 = xT3Ch * yT1Ch * zT2Ch / (1-zT3Ch) / (1-zT1Ch-xT1Ch) //  3 and z

gen T6Z = ( T3Z12 + T3Z21 + T1Z32 + T1Z23 + T2Z13 + T2Z31 ) / 6
gen T2Z = ( T3Z12 + T3Z21 ) / 2
*/




