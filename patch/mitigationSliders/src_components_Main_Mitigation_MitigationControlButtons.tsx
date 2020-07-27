import React from 'react'

import { FastField, FieldProps, Field } from 'formik'
import Media from 'react-media'

import { PercentageRange } from '../../../algorithms/types/Param.types'

import Slider from '@material-ui/core/Slider';
import { makeStyles } from '@material-ui/core/styles';
import { Button } from 'reactstrap'
import _ from "lodash";

export interface MitigationTransmissionButtonsProps {
  identifier: string
  value: PercentageRange
  
}

export function MitigationTransmissionButtons({ identifier, value }: MitigationTransmissionButtonsProps) {
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

        const handleAvg = (event: any) => {    
          // console.log(value)
          setFieldValue(identifier, {'begin': (value.begin + value.end)/2.0, 'end': (value.begin + value.end)/2.0})
        };

        const handleBegin = (event: any) => {    
          setFieldValue(identifier, {'begin': value.begin, 'end': value.begin})
        };
        const handleEnd = (event: any) => {    
          setFieldValue(identifier, {'begin': value.end, 'end': value.end})
        };

        return (
          <div className={classes.root}>
         
            <Button
              id={identifier}
              name="avg"
              onClick={handleAvg}
            >
              Avg
            </Button>

            <Button
              id={identifier}
              name="avg"
              onClick={handleBegin}

            >
              Bgn
            </Button>

            <Button
              id={identifier}
              name="avg"
              onClick={handleEnd}
            >
              End
            </Button>

          </div>
        );
      }}
    </FastField>
  )
}
