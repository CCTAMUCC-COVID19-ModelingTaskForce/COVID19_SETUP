import React from 'react'

import { FastField, FieldProps } from 'formik'
import Media from 'react-media'

import { PercentageRange } from '../../../algorithms/types/Param.types'

import Slider from '@material-ui/core/Slider';
import { makeStyles } from '@material-ui/core/styles';

import _ from "lodash";

export interface MitigationTransmissionRangeProps {
  identifier: string
  value: PercentageRange
  allowPast?: boolean
}

export function MitigationTransmissionRange({ identifier, value, allowPast = true }: MitigationTransmissionRangeProps) {
  const useStyles = makeStyles({
    root: {
      width: 200,
    },
  });
  const classes = useStyles();
  
  return (
    <FastField name={identifier} className="date-picker form-control">
      {({ form: { setFieldValue } }: FieldProps<PercentageRange>) => {

        const bounce = _.debounce((newValue: number[]) => {
            setFieldValue(identifier, {'begin': newValue[0], 'end': newValue[1]})
          }, 2)
        


        const handleChange = (event: any, newValue: number[]) => {
          bounce(newValue)

        };

        return (
          <div className={classes.root}>
         
            <Slider
              id={identifier}
              value={[value.begin, value.end]}
              onChange={handleChange}
              valueLabelDisplay="auto"
              aria-labelledby="range-slider"
            />
          </div>
        );
      }}
    </FastField>
  )
}
