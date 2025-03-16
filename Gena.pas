program FastTest;

var
  time, shag, init_temp: Real;
  cp_air, g_air, t_air_inp, alfa_air, f_air, m_air: Real;
  cp_liq, g_liq, t_liq_inp, alfa_liq, f_liq, m_liq: Real;
  c_wall, m_wall: Real;
  temperatures_air, temperatures_liq, temperatures_wall, all_time: array of Real;
  t_air_out, t_liq_out, t_wall: Real;
  dt_air, dt_liq, dt_wall: Real;
  new_temp_air, new_temp_liq, new_temp_wall: Real;

begin
  time := 0.0;
  shag := 0.05;
  init_temp := 293.0;

  // Параметры воздуха
  cp_air := 1005;
  g_air := 2.487;
  t_air_inp := 301;
  alfa_air := 457.489;
  f_air := 16.2;
  m_air := g_air;

  // Параметры жидкости
  cp_liq := 1850;
  g_liq := 1.081;
  t_liq_inp := 288;
  alfa_liq := 386.752;
  f_liq := 6.009;
  m_liq := g_liq;

  // Параметры стенки
  c_wall := 2700;
  m_wall := 5;

  // Инициализация массивов
  SetLength(temperatures_air, 1);
  temperatures_air[0] := init_temp;
  SetLength(temperatures_liq, 1);
  temperatures_liq[0] := init_temp;
  SetLength(temperatures_wall, 1);
  temperatures_wall[0] := init_temp;
  SetLength(all_time, 1);
  all_time[0] := time;

  while time <= 20 do
  begin
    // Текущие температуры из предыдущего шага
    t_air_out := temperatures_air[High(temperatures_air)];
    t_liq_out := temperatures_liq[High(temperatures_liq)];
    t_wall := temperatures_wall[High(temperatures_wall)];

    // Расчет производных
    dt_air := (cp_air * g_air * (t_air_inp - t_air_out) + alfa_air * f_air * (t_wall - t_air_out)) / (cp_air * m_air);
    dt_liq := (cp_liq * g_liq * (t_liq_inp - t_liq_out) + alfa_liq * f_liq * (t_wall - t_liq_out)) / (cp_liq * m_liq);
    dt_wall := (alfa_air * f_air * (t_air_out - t_wall) + alfa_liq * f_liq * (t_liq_out - t_wall)) / (c_wall * m_wall);

    // Обновление времени
    time := time + shag;

    // Расчет новых температур
    new_temp_air := temperatures_air[High(temperatures_air)] + dt_air * shag;
    new_temp_liq := temperatures_liq[High(temperatures_liq)] + dt_liq * shag;
    new_temp_wall := temperatures_wall[High(temperatures_wall)] + dt_wall * shag;

    // Добавление новых значений в массивы
    SetLength(temperatures_air, Length(temperatures_air) + 1);
    temperatures_air[High(temperatures_air)] := new_temp_air;
    SetLength(temperatures_liq, Length(temperatures_liq) + 1);
    temperatures_liq[High(temperatures_liq)] := new_temp_liq;
    SetLength(temperatures_wall, Length(temperatures_wall) + 1);
    temperatures_wall[High(temperatures_wall)] := new_temp_wall;
    SetLength(all_time, Length(all_time) + 1);
    all_time[High(all_time)] := time;
  end;

  WriteLn('First 10 air temperatures:');
  for var i := 0 to 9 do
    WriteLn('[', i, '] ', temperatures_air[i]:0:4);
  
  WriteLn(#13#10'First 10 liq temperatures:');
  for var i := 0 to 90 do
    WriteLn('[', i, '] ', temperatures_liq[i]:0:4);
  
  // Вывод последних 10 значений
  WriteLn(#13#10'Last 10 air temperatures:');
  for var i := High(temperatures_air)-9 to High(temperatures_air) do
    WriteLn('[', i, '] ', temperatures_air[i]:0:4);
  
  WriteLn(#13#10'Last 10 liq temperatures:');
  for var i := High(temperatures_liq)-90 to High(temperatures_liq) do
    WriteLn('[', i, '] ', temperatures_liq[i]:0:4);
end.