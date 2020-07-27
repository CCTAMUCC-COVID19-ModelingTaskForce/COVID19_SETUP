import React from 'react'

import { useTranslation } from 'react-i18next'
import { connect } from 'react-redux'
import { Col, Row } from 'reactstrap'
import { ActionCreator } from 'typescript-fsa'

import FormSwitch from '../../Form/FormSwitch'
import KrellSpinBox from '../../Form/KrellSpinBox'

import type { State } from '../../../state/reducer'

import {
  selectIsLogScale,
  selectShouldFormatNumbers,
  selectIsAutorunEnabled,
  selectPlotYMax,
  selectPlotXMax,
  selectPlotYMin,
  selectPlotXMin,
} from '../../../state/settings/settings.selectors'

import { 
  setAutorun, 
  setFormatNumbers, 
  setLogScale,
  setPlotYMax,
  setPlotXMax,
  setPlotYMin,
  setPlotXMin
} from '../../../state/settings/settings.actions'


export interface SettingsControlsProps {
  isAutorunEnabled: boolean
  isLogScale: boolean
  setAutorun: ActionCreator<boolean>
  setFormatNumbers: ActionCreator<boolean>
  setLogScale: ActionCreator<boolean>
  shouldFormatNumbers: boolean
  plotYMax: number
  plotXMax: number
  plotYMin: number
  plotXMin: number
  setPlotYMax: ActionCreator<number>
  setPlotXMax: ActionCreator<number>
  setPlotYMin: ActionCreator<number>
  setPlotXMin: ActionCreator<number>
}

const mapStateToProps = (state: State) => ({
  isAutorunEnabled: selectIsAutorunEnabled(state),
  isLogScale: selectIsLogScale(state),
  shouldFormatNumbers: selectShouldFormatNumbers(state),
  plotYMax: selectPlotYMax(state),
  plotXMax: selectPlotXMax(state),
  plotYMin: selectPlotYMin(state),
  plotXMin: selectPlotXMin(state)
})

const mapDispatchToProps = {
  setAutorun,
  setFormatNumbers,
  setLogScale,
  setPlotYMax,
  setPlotXMax,
  setPlotYMin,
  setPlotXMin,
}

export function SettingsControlsDisconnected({
  isAutorunEnabled,
  isLogScale,
  setAutorun,
  setFormatNumbers,
  setLogScale,
  shouldFormatNumbers,
  plotYMax,
  plotXMax,
  plotYMin,
  plotXMin,
  setPlotYMax,
  setPlotXMax,
  setPlotYMin,
  setPlotXMin,
}: SettingsControlsProps) {
  const { t } = useTranslation()

  return (
    <div>
    <Row noGutters className="mt-1 ml-2">
      <Col className="d-flex flex-wrap my-auto">
        <span className="mr-4 flex-1" data-testid="AutorunSwitch">
          <FormSwitch
            identifier="autorun"
            label={t('Run automatically')}
            help={t('Run simulation automatically -- when any of the parameters change')}
            checked={isAutorunEnabled}
            onValueChanged={setAutorun}
          />
        </span>
        <span className="mr-4 flex-1" data-testid="LogScaleSwitch">
          <FormSwitch
            identifier="logScale"
            label={t('Log scale')}
            help={t('Toggle between logarithmic and linear scale on vertical axis of the plot')}
            checked={isLogScale}
            onValueChanged={setLogScale}
          />
        </span>
        <span className="flex-1" data-testid="HumanizedValuesSwitch">
          <FormSwitch
            identifier="showHumanized"
            label={t('Format numbers')}
            help={t('Show numerical results in a human-friendly format')}
            checked={shouldFormatNumbers}
            onValueChanged={setFormatNumbers}
          />
        </span>
      </Col>
    </Row>
    <Row noGutters className="mt-1 ml-2">
      <Col className="d-flex flex-wrap my-auto">
        Y-lower:
        <KrellSpinBox 
          identifier="plotYMin"
          changeEvent={setPlotYMin}
          min={0}
          step={50}
        />
      </Col>
      <Col className="d-flex flex-wrap my-auto">
        Y-upper: 
        <KrellSpinBox 
          identifier="plotYMax"
          changeEvent={setPlotYMax}
          min={0}
          step={50}
        />
       (Enter 0 for MAX)
       </Col>
     </Row>
     <Row noGutters className="mt-1 ml-2">
       <Col className="d-flex flex-wrap my-auto">
         X-lower:
         <KrellSpinBox 
          identifier="plotYMin"
          changeEvent={setPlotXMin}
          min={0}
          step={1}
        />
       </Col>
       <Col className="d-flex flex-wrap my-auto">
         X-upper: 
         <KrellSpinBox 
          identifier="plotXMax"
          changeEvent={setPlotXMax}
          min={0}
          step={1}
        />
        (Enter 0 for MAX)
      </Col>
    </Row>
    </div>
  )
}

const SettingsControls = connect(mapStateToProps, mapDispatchToProps)(SettingsControlsDisconnected)

export { SettingsControls }
