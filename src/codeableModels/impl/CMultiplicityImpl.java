package codeableModels.impl;

import codeableModels.*;

public class CMultiplicityImpl implements CMultiplicity {
    private int upperMultiplicity, lowerMultiplicity;
    private String multiplicityString;

    public CMultiplicityImpl(String multiplicity) throws CException {
        setMultiplicity(multiplicity);
        multiplicityString = multiplicity;
    }

    /*
    public CMultiplicityImpl(int lower, int upper) {
        this.upperMultiplicity = upper;
        this.lowerMultiplicity = lower;
    }
    */

    private void setMultiplicity(String multiplicity) throws CException {
        try {
            String lowerStr, upperStr;
            if (multiplicity.contains("..")) {
                lowerStr = multiplicity.replaceFirst("..([^.]*)$", "").trim();
                upperStr = multiplicity.replaceFirst("^([^.]*)..", "").trim();
                lowerMultiplicity = Integer.parseInt(lowerStr);
                if (lowerMultiplicity < 0) {
                    throw new CException("negative multiplicity in '"
                            + multiplicity + "'");
                }
                if (upperStr.equals("*")) {
                    upperMultiplicity = STAR_MULTIPLICITY;
                } else {
                    upperMultiplicity = Integer.parseInt(upperStr);
                    if (upperMultiplicity < 0) {
                        throw new CException("negative multiplicity in '"
                                + multiplicity + "'");
                    }
                }
            } else if (multiplicity.trim().equals("*")) {
                lowerMultiplicity = 0;
                upperMultiplicity = STAR_MULTIPLICITY;
            } else {
                lowerMultiplicity = Integer.parseInt(multiplicity.trim());
                if (lowerMultiplicity < 0) {
                    throw new CException("negative multiplicity in '"
                            + multiplicity + "'");
                }
                upperMultiplicity = lowerMultiplicity;
            }
        } catch (Exception e) {
            if (e instanceof CException) {
                throw (CException) e;
            }
            throw new CException("malformed multiplicity '" + multiplicity
                    + "'");
        }
    }

    @Override
    public String getMultiplicity() {
        if (lowerMultiplicity == 0 && upperMultiplicity == STAR_MULTIPLICITY) {
            return "*";
        }
        StringBuilder r = new StringBuilder();
        r.append(lowerMultiplicity);
        if (lowerMultiplicity != upperMultiplicity) {
            r.append("..");
            if (upperMultiplicity == STAR_MULTIPLICITY) {
                r.append("*");
            } else {
                r.append(upperMultiplicity);
            }
        }
        return r.toString();
    }

    @Override
    public int getUpperMultiplicity() {
        return upperMultiplicity;
    }

    @Override
    public int getLowerMultiplicity() {
        return lowerMultiplicity;
    }

    public String toString() {
        return multiplicityString;
    }

}
