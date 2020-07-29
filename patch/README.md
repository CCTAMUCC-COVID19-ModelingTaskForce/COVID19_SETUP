## Patch files
This directory contains files that replace files in `neherlab/covid19_scenarios`.
They should work with version 1.8.0 (commit: `c6e611bcc87f01a8160530cf74f4e8e3ea1f0b0f`).

#### Patch `plotControls`: control plot axes 

Adds spinboxes to select min and max values for x and y axes.

	# Backup originals
	cp ../../src/state/settings/settings.actions.ts \
		plotControls/src_state_settings_settings.actions.ts.orig
	cp ../../src/state/settings/settings.reducer.ts \
		plotControls/src_state_settings_settings.reducer.ts.orig
	cp ../../src/state/settings/settings.sagas.ts \
		plotControls/src_state_settings_settings.sagas.ts.orig
	cp ../../src/state/settings/settings.selectors.ts \
		plotControls/src_state_settings_settings.selectors.ts.orig
	cp ../../src/state/settings/settings.state.ts \
		plotControls/src_state_settings_settings.state.ts.orig
	cp ../../src/components/Main/Controls/SettingsControls.tsx \
		plotControls/src_components_Main_Controls_SettingsControls.tsx.orig
	cp ../../src/components/Main/Results/DeterministicLinePlot.tsx \
		plotControls/src_components_Main_Results_DeterministicLinePlot.tsx.orig

	# Replace with patched
	cp plotControls/src_state_settings_settings.actions.ts \ 
		../../src/state/settings/settings.actions.ts
	cp plotControls/src_state_settings_settings.reducer.ts \
		../../src/state/settings/settings.reducer.ts
	cp plotControls/src_state_settings_settings.sagas.ts \
		../../src/state/settings/settings.sagas.ts
	cp plotControls/src_state_settings_settings.selectors.ts \
		../../src/state/settings/settings.selectors.ts
	cp plotControls/src_state_settings_settings.state.ts \
		../../src/state/settings/settings.state.ts
	cp plotControls/src_components_Form_KrellSpinBox.tsx \
		../../src/components/Form/KrellSpinBox.tsx
	cp plotControls/src_components_Main_Controls_SettingsControls.tsx \
		../../src/components/Main/Controls/SettingsControls.tsx
	cp plotControls/src_components_Main_Results_DeterministicLinePlot.tsx \
		../../src/components/Main/Results/DeterministicLinePlot.tsx


#### Patch `mitigationSliders`: slider control of mitigations

	# Backup originals
	cp ../../src/components/Main/Mitigation/MitigationDatePicker.tsx \
		mitigationSliders/src_components_Main_Mitigation_MitigationDatePicker.tsx.orig
	cp ../../src/components/Main/Mitigation/MitigationIntervalComponent.tsx \
		mitigationSliders/src_components_Main_Mitigation_MitigationIntervalComponent.tsx.orig
	cp ../../src/components/Main/Mitigation/MitigationTable.scss \
		mitigationSliders/src_components_Main_Mitigation_MitigationTable.scss.orig
	cp ../../src/components/Main/Mitigation/MitigationTable.tsx \
		mitigationSliders/src_components_Main_Mitigation_MitigationTable.tsx.orig

	# Replace with patches
	cp mitigationSliders/src_components_Main_Mitigation_MitigationDatePicker.tsx \
		../../src/components/Main/Mitigation/MitigationDatePicker.tsx
	cp mitigationSliders/src_components_Main_Mitigation_MitigationIntervalComponent.tsx \
		../../src/components/Main/Mitigation/MitigationIntervalComponent.tsx
	cp mitigationSliders/src_components_Main_Mitigation_MitigationTable.scss \
		../../src/components/Main/Mitigation/MitigationTable.scss
	cp mitigationSliders/src_components_Main_Mitigation_MitigationTable.tsx \
		../../src/components/Main/Mitigation/MitigationTable.tsx
	cp mitigationSliders/src_components_Main_Mitigation_MitigationControlButtons.tsx \
		../../src/components/Main/Mitigation/MitigationControlButtons.tsx
	cp mitigationSliders/src_components_Main_Mitigation_MitigationTransmissionRange.tsx \
		../../src/components/Main/Mitigation/MitigationTransmissionRange.tsx
	cp mitigationSliders/src_components_Main_Mitigation_RangeSlider.tsx \
		../../src/components/Main/Mitigation/RangeSlider.tsx


#### Patch `trajectories`: additional data on Outbreak Trajectories plot

	# Backup originals
	cp ../../src/algorithms/preparePlotData.ts \
		trajectories/src_algorithms_preparePlotData.ts.orig
	cp ../../src/algorithms/results.ts \
		trajectories/src_algorithms_results.ts.orig
	cp ../../src/algorithms/model.ts \
		trajectories/src_algorithms_model.ts.orig
	cp ../../src/algorithms/run.ts \
		trajectories/src_algorithms_run.ts.orig
	cp ../../src/algorithms/types/Result.types.ts \
		trajectories/src_algorithms_types_Result.types.ts.orig
	cp ../../src/components/Main/Results/ChartCommon.ts \
		trajectories/src_components_Main_Results_ChartCommon.ts.orig
	cp ../../src/components/Main/Results/DeterministicLinePlot.tsx \
		trajectories/src_components_Main_Results_DeterministicLinePlot.tsx.orig

	# Replace with patches
	cp trajectories/src_algorithms_preparePlotData.ts \
		../../src/algorithms/preparePlotData.ts
	cp trajectories/src_algorithms_results.ts \
		../../src/algorithms/results.ts
	cp trajectories/src_algorithms_model.ts \
		../../src/algorithms/model.ts
	cp trajectories/src_algorithms_run.ts \
		../../src/algorithms/run.ts
	cp trajectories/src_algorithms_types_Result.types.ts \
		../../src/algorithms/types/Result.types.ts 
	cp trajectories/src_components_Main_Results_ChartCommon.ts \
		../../src/components/Main/Results/ChartCommon.ts
	cp trajectories/src_components_Main_Results_DeterministicLinePlot.tsx \
		../../src/components/Main/Results/DeterministicLinePlot.tsx

