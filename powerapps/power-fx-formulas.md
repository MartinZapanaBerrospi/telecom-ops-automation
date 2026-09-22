# Fórmulas Power Fx

Las fórmulas de la Canvas App, una por propiedad de control. Cada bloque indica entre
paréntesis dónde va pegada.

Los nombres de control siguen las [convenciones del README](README.md#convenciones-de-nombres)
y los nombres de tabla y columna vienen de
[`docs/02-data-model.md`](../docs/02-data-model.md): si al construir la app usas otros,
hay que ajustar las fórmulas.

| Fórmula | Propiedad | Regla que implementa |
|---|---|---|
| [1. Inicialización](#1-inicialización-de-la-aplicación-apponstart) | `App.OnStart` | — |
| [2. Búsqueda de recibo](#2-auto-relleno-de-datos-al-buscar-recibo-txtnumeroreciboonchange) | `txtNumeroRecibo.OnChange` | **R5** |
| [3. Envío de solicitud](#3-registro-y-envío-de-solicitud-con-validación-btnenviarsolicitudonselect) | `btnEnviarSolicitud.OnSelect` | **R1** |
| [4. Filtrado de galería](#4-filtrado-dinámico-de-galería-galajustesitems) | `galAjustes.Items` | — |

---

### 1. Inicialización de la Aplicación (`App.OnStart`)
```powerfx
// Cargar perfil del usuario actual y rol operacional
Set(varCurrentUser, User());
Set(
    varIsJefatura, 
    varCurrentUser.Email in ["jefatura.postfacturacion@telecom.com", "supervisor.ops@telecom.com"]
);

// Cargar colección de ajustes y caché de catálogos
ClearCollect(
    colAjustes,
    AjustesPostFacturacion
);

ClearCollect(
    colCiclos,
    Table(
        { Codigo: "C01", Nombre: "Ciclo 01 (Corte 01)" },
        { Codigo: "C15", Nombre: "Ciclo 15 (Corte 15)" },
        { Codigo: "C28", Nombre: "Ciclo 28 (Corte 28)" }
    )
);
```

---

### 2. Auto-relleno de Datos al Buscar Recibo (`txtNumeroRecibo.OnChange`)
```powerfx
// Buscar factura en la base de datos y extraer información del cliente
Set(
    varFacturaEncontrada,
    LookUp(
        FacturasEmitidas,
        NumeroRecibo = Trim(txtNumeroRecibo.Text)
    )
);

If(
    !IsBlank(varFacturaEncontrada.IdFactura),
    // Factura encontrada: auto-llenar campos
    UpdateContext({
        varClienteNombre: varFacturaEncontrada.ClienteNombre,
        varPlanNombre: varFacturaEncontrada.PlanNombre,
        varMontoOriginal: varFacturaEncontrada.MontoTotal,
        varFacturaValida: true
    });
    Notify("Factura validada correctamente en el sistema.", NotificationType.Success, 2000),
    
    // Factura no existe
    UpdateContext({
        varClienteNombre: "",
        varPlanNombre: "",
        varMontoOriginal: 0,
        varFacturaValida: false
    });
    Notify("El número de recibo no existe en el ciclo actual.", NotificationType.Error, 3000)
);
```

---

### 3. Registro y Envío de Solicitud con Validación (`btnEnviarSolicitud.OnSelect`)
```powerfx
// Validar que el monto no exceda la factura y justificación sea completa
If(
    Value(txtMontoSolicitado.Text) <= 0 Or Value(txtMontoSolicitado.Text) > varMontoOriginal,
    Notify("El monto solicitado no puede ser mayor al total de la factura.", NotificationType.Error, 4000),
    
    If(
        Len(txtJustificacion.Text) < 15,
        Notify("Debe ingresar una justificación técnica detallada.", NotificationType.Warning, 3000),
        
        // Guardar registro mediante Patch
        Set(
            varNuevoAjuste,
            Patch(
                AjustesPostFacturacion,
                Defaults(AjustesPostFacturacion),
                {
                    IdFactura: varFacturaEncontrada.IdFactura,
                    NumeroRecibo: txtNumeroRecibo.Text,
                    IdCliente: varFacturaEncontrada.IdCliente,
                    ClienteNombre: varClienteNombre,
                    TipoIncidencia: drpTipoIncidencia.Selected.Value,
                    MontoReclamado: Value(txtMontoSolicitado.Text),
                    MontoReconocido: 0,
                    EstadoReclamo: "PENDIENTE_APROBACION",
                    UsuarioAnalista: varCurrentUser.Email,
                    FechaRegistro: Now(),
                    Justificacion: txtJustificacion.Text
                }
            )
        );
        
        // Disparar flujo en Power Automate para notificación a jefatura
        FlowNotificarAprobacionAjuste.Run(
            varNuevoAjuste.IdAjuste,
            txtNumeroRecibo.Text,
            varClienteNombre,
            Value(txtMontoSolicitado.Text),
            drpTipoIncidencia.Selected.Value,
            varCurrentUser.FullName
        );
        
        Notify("Solicitud enviada a aprobación exitosamente.", NotificationType.Success, 3000);
        Navigate(DashboardScreen, ScreenTransition.Fade)
    )
);
```

---

### 4. Filtrado Dinámico de Galería (`galAjustes.Items`)
```powerfx
SortByColumns(
    Filter(
        colAjustes,
        (IsBlank(txtBuscador.Text) Or txtBuscador.Text in NumeroRecibo Or txtBuscador.Text in ClienteNombre) And
        (drpFiltroEstado.Selected.Value = "TODOS" Or EstadoReclamo = drpFiltroEstado.Selected.Value)
    ),
    "FechaRegistro",
    SortOrder.Descending
)
```
