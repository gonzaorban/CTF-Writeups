-- ============================================================================
-- Respaldo automático de la base "nominet" — Panel RRHH NómiNet
-- Generado por el script de backup nocturno (cron). NO DEBE QUEDAR PÚBLICO.
-- Contiene la tabla de usuarios con sus hashes de contraseña.
-- ============================================================================

CREATE TABLE usuarios (
  id            INTEGER PRIMARY KEY,
  usuario       TEXT NOT NULL UNIQUE,
  nombre        TEXT,
  rol           TEXT,
  password_hash TEXT NOT NULL
);

-- Las contraseñas se guardan con sha512crypt ($6$), el mismo esquema que
-- /etc/shadow en Linux. "Hasheadas = seguras", decía el que las eligió...
INSERT INTO usuarios (id, usuario, nombre, rol, password_hash) VALUES
  (1, 'admin', 'Soporte TI', 'admin', '$6$lab64adm$Guw66KEaFrRz0Itikk4AskR7aODQ/ZQ.nVlE.Wls5KIuyTu5abF.7I6oJENqCgtnvB1EsdUUDrGzqiP9zq0FU0'),
  (2, 'mlopez', 'María López', 'rrhh', '$6$lab64mlo$1i33ZIIfUrjAiR8vueIIbcV8kOawU./ba7yXjicjvq7RlaMABDzruyNtLbqjq5DQ1AXm8Gwf92sx1Ud8pN0cO.'),
  (3, 'jgomez', 'Julián Gómez', 'rrhh', '$6$lab64jgo$pDZT7zY6tdSDw1nVlVmKSx1aulaIsVBMKH5WtjF258uDT.LimWfXoWigaMDcYBAoaT.cAVvnu1pnrtKzRaroa0'),
  (4, 'rh_junior', 'Pasante RRHH', 'lectura', '$6$lab64rhj$ebL/BJXLvT6.XeIHamu2fbdXopQ7Y2ybShcPIW2DJ7pcf94hQZKZ7wlk45dGHVFzCf0rffu9ZJ/BSiYNL7jPb0'),
  (5, 'cfernandez', 'Carla Fernández', 'rrhh', '$6$lab64u05$BZQrg7tFqQYGMu9YMozitzC4UC.2klsX8UaBpMvfk90u6VrZFqj45XIjlNJFm7jmK.C2kH2CxxxkdANQuU0dy.'),
  (6, 'dramirez', 'Diego Ramírez', 'nomina', '$6$lab64u06$lSPvzhnhMz4n/vJs1y2tcIG0ZNil/jyufyo3dS9.xno7AXi9oyqf7zjgsQ8HIZXM9OoXNmkFN94ku8g0olgEp1'),
  (7, 'lsosa', 'Lucía Sosa', 'legajos', '$6$lab64u07$TnIQByxqHnp7mHcGqGMmsmfkq1q5nmSPZghVpzc7hLNGqGRbVslZ.1jKF55gqbLYutshDPPTzmWfduPAi.8qy1'),
  (8, 'pmartinez', 'Pablo Martínez', 'contable', '$6$lab64u08$8x4EeWwGW28fCVYn3bDKRGrERPl1pKAXfGuOKoDvJwjWsAjm5fFakxFLJM.fSnFVSp.YlgkV0RFBR8gaR.t5R.'),
  (9, 'agonzalez', 'Ana González', 'reclutamiento', '$6$lab64u09$drT6OZHGtqQ99WxqvilCx/C5T0RtryTjEToItiFywzbfMzf9ZqGKfO1/EfYU4B/knUTTnNdh1ycD.oB4TtEgq1'),
  (10, 'rdiaz', 'Rodrigo Díaz', 'soporte', '$6$lab64u10$ZHjCg50JOKLaG2SwwQMOIAr8HqGbDBA0bUSg3X9XvWpn/ZJpUKGMLzaSqtpmw1vQiY3Hkgja8o1xBjU49bCXx.'),
  (11, 'vtorres', 'Valentina Torres', 'rrhh', '$6$lab64u11$Ra2EHFpzVmAwefT2lBW/2.KqGV0ujc3DBbNcFuCiJmqT9nItsrihLXlXmlhICW2HWLajUEUjnvZcxdKqhwGSL.'),
  (12, 'nacosta', 'Nicolás Acosta', 'lectura', '$6$lab64u12$Ugczw20.4SEE8dXAzrwxLH2xo87BbIgWGesGTqCn5M5xX9c0I5yzDMB9UciGmN2RZ.N2JwmAk9ZueW0tTZ9qq0'),
  (13, 'sromero', 'Sofía Romero', 'nomina', '$6$lab64u13$QSgbg8g4Nqy1byql3dgn/bWnbcx/c855jzkmup.bMwW7/DN4I0Cst2NEd9425d17FSgwmZbHmWdj704UPGKCB/'),
  (14, 'fbenitez', 'Facundo Benítez', 'legajos', '$6$lab64u14$SYm2bl/m.eudgbgJbbNLIXmy5FREIqiAJ6t26Iui8TsoYDBDA72no9K5RkNt4GyzCim8IdEMmzOt/ac1jh6qO0'),
  (15, 'mcastro', 'Micaela Castro', 'rrhh', '$6$lab64u15$3mX1tRBOWPRal1XZMwJbPuTcFLnO/.E9e.34j6qtT20X8kpuMX3YmNjAGlcvtysxnKxMQgZVCUR5P775Kl2Vf/'),
  (16, 'gherrera', 'Gastón Herrera', 'contable', '$6$lab64u16$MdAgADWA6.m.qZRBjFNjj7saY/32XlRR0VpkU1LYrbe0JhqAL3wJzeJdfneWmJRSSsX6Q8uHgpcSbc0vfT7Xw1'),
  (17, 'bmorales', 'Brenda Morales', 'lectura', '$6$lab64u17$E1xJzwXAtsKF1XGU9EoJYQAVwx7Up5GW5phaanMw7AsHBGoE9qSv6HhDReMnMNYgYLGQ9IzfnEdhR5OdWggnF.'),
  (18, 'jsilva', 'Joaquín Silva', 'soporte', '$6$lab64u18$U23uzv4TeDpkhRCcnO3jGeoXGUgRbe8r132dUa0s7Dm..u0Pf/zJXUTBvSjqRyLJo8px8pxTFCdXqpesZlUvR0'),
  (19, 'creyes', 'Camila Reyes', 'reclutamiento', '$6$lab64u19$VaqdbEuIftTIlncej.Vj5gvNn7rWrKbZk1x3/eSOSQb51gvBFVDqatGXnychgX67pscf9qlHDbBrZKSoK.LtF/'),
  (20, 'earias', 'Emiliano Arias', 'nomina', '$6$lab64u20$rB9YGeTMiZuvbFIrLv2U2p6yHKPplMjAmseokFcfgE8I/SpoVckLmO5Wie.C/LsZ0cwQo.rvAZe6tsd0OnBCw1'),
  (21, 'pmendez', 'Paula Méndez', 'rrhh', '$6$lab64u21$FSSt/NEsyKX8JE9M.Cq2lVGJ.InTy01fd26M/lRgCuKtpTmlB5OIbrILhXhn40xi2athpaE2hyvgd9xDt7a05/'),
  (22, 'lvega', 'Lautaro Vega', 'legajos', '$6$lab64u22$kNhSZcJqzG3UnP9VzmP53PNYr7V5mgYCHkZniMhdYtKXnLj4tZ08kd39ZY7Z7G.WnYx1sgWu95jjOEKLzr73Y.'),
  (23, 'drojas', 'Daniela Rojas', 'lectura', '$6$lab64u23$0fbsqiLMurxpmtHQ08rV6fQZXSaUrF0jblYjVKf03ITWZbi56Wa8Gjr4ws4DoIVCOoDSlF0IbNKIiUueVeEO5.'),
  (24, 'mnunez', 'Matías Núñez', 'contable', '$6$lab64u24$5ORHcBnHASfyS4OC8PtIOWdQj81WGUqwTWyqeqxiY2DUweFCJ8xsmnZYLlc2ICYsFIyb.AD/2iIzqo1oL/UML/'),
  (25, 'afigueroa', 'Agustina Figueroa', 'rrhh', '$6$lab64u25$MkqXJdtLiw1famCtzWCU2iahHCNi1NlOtB0/nmOvUlyNrrDfDpHDGnmEuhJDjqT1.Lfrr8poGR07j0DapjE9d1'),
  (26, 'gcabrera', 'Gonzalo Cabrera', 'soporte', '$6$lab64u26$k7yLgCogfWpMQKnNURSIwmNw61rWjHAq8kDlWTvL26mngtSO2yB9nglqwdH94Dh1k2M8ZYUI0p0KGNbXvDd2d.'),
  (27, 'rmolina', 'Rocío Molina', 'nomina', '$6$lab64u27$LEAEUiY7wGVCR3tI/zLc3b1ZofOxfnivVIBZf12ZI96SchJXmerNyrXYp926KbtsS3HRoZYvMK38KsEM4nMK9.'),
  (28, 'tgutierrez', 'Tomás Gutiérrez', 'legajos', '$6$lab64u28$twEb4e4bEZbXirYQs4eB.Ht7Q0AwU7YWwmP6zNtk6JRw6cX7cJBHxT2kLeV.MBAgEBkKLCXjsZ.M6ARfgLPnV.'),
  (29, 'jsuarez', 'Julieta Suárez', 'lectura', '$6$lab64u29$oY6vjDuwdqFMC5pmBrGrjeatVLXaSXcOimS.l3tDTcfM58oEKIAaCgEMJaFwYrUGNR22tH5b8hkbNhx7moXsN.'),
  (30, 'fcardozo', 'Franco Cardozo', 'reclutamiento', '$6$lab64u30$AemuqAGXEemK7IipQrn31UB.Rhp1fbzug/ydC0mw.zEmOzkXhn6oPFblfdYbohS96su/R.Z08ZM6ImepUr5v60'),
  (31, 'mperalta', 'Melina Peralta', 'rrhh', '$6$lab64u31$x/FMF3wbDsUOBtXE9Tc8uYLb719ZYst7PtO6QCWGTpt78kXRmOzKPsFZAH9h6VHJSWaQxAcniake35FjkncdB/'),
  (32, 'ndominguez', 'Nahuel Domínguez', 'contable', '$6$lab64u32$39Ex9hDg0Rzd14kF5NXfll1b4HoJAxkyAuz8EXSUSpjdinYvpEuoYGZPrRxDMB9/Fclzaum.y7u2xWWstadMl0'),
  (33, 'cvera', 'Candela Vera', 'lectura', '$6$lab64u33$Aurp2R2NZ.eHzv1dnMe7iX5d7IUDTNUnp7eqOzrSt.IYEj9IBYJUyf8aL0cE2Eekwry2YjO6zDjJAH0qE64Jl/'),
  (34, 'iluna', 'Ignacio Luna', 'soporte', '$6$lab64u34$S1aYfzR5S4Tr7EChoZxmw1SNSocTNri45tZo6vAFYiIuOEd6TBfX5r051hPJ0UnvQPjFtcduC1fVx4YIeR.8M.'),
  (35, 'gmaldonado', 'Giuliana Maldonado', 'nomina', '$6$lab64u35$/7LWSsMFEB.QwJg6DCGY2jPFKJCryEDfKmXl.a6jEtN37xyO56tVQ6LpQq1/kcQhiB92i.ndmuhBrq/7nUalb1'),
  (36, 'fojeda', 'Federico Ojeda', 'legajos', '$6$lab64u36$DAB3pS91ID0dz039Ypq/Tw6G/Ukh5wuv/2cRneHvtuVYlqRmQOPILXA6LbUMZnkGkpoG0CY.rPRwj/Q7boxKY1'),
  (37, 'abravo', 'Aldana Bravo', 'rrhh', '$6$lab64u37$mvSsjjA2XuC1u1CyhXIW1.c30Ao3caTlvKvTiLH3YpfOwd6QCgDmnDgxY/9RNSlAt0EiMqN2XbmSm/F4a6SNW.'),
  (38, 'mrios', 'Maximiliano Ríos', 'lectura', '$6$lab64u38$CORqxGrswpFfZfUCDFzC4kvP3yWsUXsoTCLPT7KDUiGcqyDIJyHgJLznn.0oqNPxqoQWVTagf3V8iJOcJ4HuY1'),
  (39, 'pcampos', 'Priscila Campos', 'contable', '$6$lab64u39$Xd8Hgc/z7hdyF.BXqHR6RPouWNPZ7DTeU/dn1UTD7GGSmThsyVdb0zC9mMBbpjojLPLa5XFWuopIowCM6OzN/1'),
  (40, 'dcaceres', 'Damián Cáceres', 'soporte', '$6$lab64u40$qwpH4oDx4IEfAJGphqNgWk3ramzQthqJuGv5fao.F.QtrjRtWNBGZk4W4GRbQbqvGPIiC8VGSuTpU./CYLGMx/'),
  (41, 'smiranda', 'Samantha Miranda', 'nomina', '$6$lab64u41$MEhrSfpqxnkluNU5aGHDJnT474UmvP2MS0DDPKDNrWpjqmZSfDRbmya9YU0b4ej7LuFSmW2yu.wbRRaJJV3AH1'),
  (42, 'ocordoba', 'Octavio Córdoba', 'legajos', '$6$lab64u42$mdFGSqimcvF1mMZI/.q.RPp9qBh31w3HZBzoibK3v7vuoyFtZponk2qG0Dr.U0Rkls885N9/kK8XdqhrWzMT2.'),
  (43, 'lferreyra', 'Lorena Ferreyra', 'rrhh', '$6$lab64u43$OJSPEuSQ/0cOEFapx6.xfpveaT9SLwq/cfk8fCJm0PHypDP79RNB0WQmNdyv2YAdhf8WPm3nr47NUOqVZ45ss0'),
  (44, 'bgimenez', 'Bruno Giménez', 'lectura', '$6$lab64u44$OxZ6cd5ngpwahGEFGfKyCFF444VmYj0E44kiGmLroNkJU7svY4GRzc1bWCv6U3dRUjh8TzIgWK4oveE4OtqyL1'),
  (45, 'mquiroga', 'Milagros Quiroga', 'reclutamiento', '$6$lab64u45$3NAFkjalhC4ed3dAAiw4YVxBvVeKCjZ7DNN0jQ.nhOY/aDM40AukEgcsBjSNWQFt0LORRYdmDOLY2ekpYT9BN0'),
  (46, 'rvargas', 'Ramiro Vargas', 'contable', '$6$lab64u46$50WEOxgrzmmspzmciEN6AGcSHurWcegLz4YkF02v/Khvit/cgL1/mIUR.Qn3RQAbG3IwMaG6bF86hTD2Xrh6O.'),
  (47, 'ncarrizo', 'Noelia Carrizo', 'nomina', '$6$lab64u47$EMP6leSTe7iltP5Q1h4yQ0AEPbEIu/fi/TIzlWLpgsmLAjIefg1nVoZPaLrpPtuOY5yYsTfldmBOpQ/NJoWIT/'),
  (48, 'fpaez', 'Fabián Páez', 'soporte', '$6$lab64u48$mFQhEx.bBDJ9bwygKSDoxNS2bzllphmQmQTf7gZVJg.h0HfrBO/5rjVhV1mWYuXoAtAAJzs34TcMEvb9WvZFQ.'),
  (49, 'caguirre', 'Celeste Aguirre', 'legajos', '$6$lab64u49$HbkZCnb5RYL57eMVopAM.4CJkpTO4LQfjADtPIs7TWMU7nd.90EoEJRqVaT.RGTQmlwfPnZ230uGCVn2dVYo00'),
  (50, 'hmedina', 'Hernán Medina', 'lectura', '$6$lab64u50$ONlrCAah1uI0PHfQwzoa6/soVAQ1qP.TzQ6Vdk9WQuddogobWUFbdSzTsdbScLQ91sZhatbFZ1Cpe0rKWyQDz1');
