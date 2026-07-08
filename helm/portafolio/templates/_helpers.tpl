{{- define "portafolio.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "portafolio.labels" -}}
app.kubernetes.io/name: {{ include "portafolio.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "portafolio.databaseUrl" -}}
postgres://{{ .Values.postgres.user }}:{{ .Values.postgres.password }}@{{ .Release.Name }}-postgres:5432/{{ .Values.postgres.db }}
{{- end -}}
