import React from 'react'
import {Field} from 'formik'
import { CustomInput } from 'reactstrap'

export interface KrellSpinBoxProps {
  identifier: string
  min: number
  step: number
  changeEvent(e: any): void
}

export default function KrellSpinBox({
  identifier,
  min, 
  step,
  changeEvent,
  ...props
}: KrellSpinBoxProps) {
  return (
    <Field
      type="number"
      min={min}
      step={step}
      id={identifier}
      name={identifier}
      onChange={(e : any)=> {changeEvent(e.target.value)}}
      {...props}
    />
  )
}
