# ⚡ Biblioteca de Fórmulas Power Fx
### Funciones Core implementadas en la aplicación de Post Facturación

---

### 1. Inicialización de la Aplicación (`App.OnStart`)
```powerfx
// Cargar perfil del usuario actual y rol operacional
Set(varCurrentUser, User());
Set(
    varIsJefatura, 
    varCurrentUser.Email in ["jefatura.postfacturacion@claro.com.pe", "supervisor.ops@claro.com.pe"]
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
