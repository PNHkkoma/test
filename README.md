//tỷ lệ tăng chưởng
    public function growth_rate(Request $request)
    {
         try
         {  //ở đây đáng lẽ lấy cùng 1 db nhưng khác request_id
            //$data = DB::table('your_table_name')->where('request_id', 'A')->get();
            $data = DB::table('your_table_name')->get();
            $data_discrepancy = DB::table('your_table_name1')->get();

            $fields = [];
            $value = [];
            // Dùng vòng for để lặp qua từng phần tử trong $data
            foreach ($data as $index => $item) {
                $value[$item->company_id] = $data_discrepancy[$index]->value == 0
                ? null
                : round($item->value / $data_discrepancy[$index]->value, 1);
                if(($index-17)%18==0) {
                    $fields[] = array_merge( [
                    'id' => $item->ID ?? null,
                    'report_name' => $item->report_name ?? null,
                    'period_id' => $item->period_id ?? null,
                    'type_period' => $item->type_period ?? null,
                    'month' => $item->month ?? null,
                    'year' => $item->year ?? null,
                    'code' => $item->code ?? null,
                    'index' => $item->index ?? null,
                    'khoan_muc_id' => $item->khoan_muc_id ?? null,
                    'total' => $data_discrepancy[$index]->total == 0
                        ? null
                        : round($item->total / $data_discrepancy[$index]->total, 1),
                    'hop_nhat' => $data_discrepancy[$index]->hop_nhat == 0
                        ? null
                        : round($item->hop_nhat / $data_discrepancy[$index]->hop_nhat, 1),
                    'hop_nhat_vtp' => $data_discrepancy[$index]->hop_nhat_vtp == 0
                        ? null
                        : round($item->hop_nhat_vtp / $data_discrepancy[$index]->hop_nhat_vtp, 1),
                    'hop_nhat_tru_lo' => $data_discrepancy[$index]->hop_nhat_tru_lo == 0
                        ? null
                        : round($item->hop_nhat_tru_lo / $data_discrepancy[$index]->hop_nhat_tru_lo, 1),
                    'vtg_no_dividend' => $data_discrepancy[$index]->vtg_no_dividend == 0
                        ? null
                        : round($item->vtg_no_dividend / $data_discrepancy[$index]->vtg_no_dividend, 1),
                    'vtg_dividend' => $data_discrepancy[$index]->vtg_dividend == 0
                        ? null
                        : round($item->vtg_dividend / $data_discrepancy[$index]->vtg_dividend, 1),
                    'vtg_net' => $data_discrepancy[$index]->vtg_net == 0
                        ? null
                        : round($item->vtg_net / $data_discrepancy[$index]->vtg_net, 1),
                    'dc_tt' => $data_discrepancy[$index]->dc_tt == 0
                        ? null
                        : round($item->dc_tt / $data_discrepancy[$index]->dc_tt, 1),
                    'dc_cltg' => $data_discrepancy[$index]->dc_cltg == 0
                        ? null
                        : round($item->dc_cltg / $data_discrepancy[$index]->dc_cltg, 1),
                    'dc_khac' => $data_discrepancy[$index]->dc_khac == 0
                        ? null
                        : round($item->dc_khac / $data_discrepancy[$index]->dc_khac, 1),
                    ],
                    ['company_id' => $value]
                    );
                    $value = [];
                }

            }

            // Trả về kết quả
            return response()->json([
                'success' => true,
                'fields' => $fields
            ]);
    } catch(Exception $e)
    {
            abort(500);
        }
    }

    //đơn vị,năm,kỳ báo cáo là lấy từ request,loại báo cáo sẽ được lấy?
    public function getTypeReport(Request $request) {
        try {
            $type_reports = [];
            $year = $request['year'];
            $typePeriod = $request['typePeriod'];
            $period = $request['period'] ?? null;
            $month = $request['month'] ?? null;
            $data = DB::table('process_requests')
                    ->where('application_id', 73)
                    ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                    ->pluck('data');

            $dataOther = DB::table('reports_import')
                    ->where('report_year', $year)
                    ->where('report_period', $typePeriod);

            if($typePeriod == 'quarter') {
                //xác định tồn tại thực hiện/kế hoạch
                $execute = $data->filter(function ($item) use ($year, $period) {
                    $decoded = json_decode($item, true);
                    return isset($decoded['loai_dl']) &&
                    $decoded['nam'] === $year &&
                    $decoded['quy'] === $period &&
                    ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                });
                $plan = $data->filter(function ($item) use ($year, $period) {
                    $decoded = json_decode($item, true);
                    return isset($decoded['loai_dl']) &&
                    $decoded['nam'] === $year &&
                    $decoded['quy'] === $period &&
                    $decoded['loai_dl'] === '1';
                });
                if ($execute->isNotEmpty() && ($plan->isNotEmpty() || $dataOther->isNotEmpty())) {
                    $type_reports[] = 'Báo cáo kỳ thực hiện với số kế hoạch';
                }

                //xác định tồn tại thực hiện/thực hiện cùng kỳ
                $executeSamePeriod = $data->filter(function ($item) use ($year, $period) {
                    $decoded = json_decode($item, true);
                    return isset($decoded['loai_dl']) &&
                    (int)$decoded['nam'] === $year - 1 &&
                    $decoded['quy'] === $period &&
                    ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                });
                if ($execute->isNotEmpty() && $executeSamePeriod->isNotEmpty()) {
                    $type_reports[] = 'Báo cáo kỳ thực hiện với cùng kỳ';
                }

                //xác định tồn tại thực hiện/ liền kề
                $adjacent = $data->filter(function ($item) use ($year, $period) {
                    $decoded = json_decode($item, true);
                    if($period == '1'){
                        return isset($decoded['loai_dl']) &&
                        (int)$decoded['nam'] === $year - 1 &&
                        $decoded['quy'] === '4' &&
                        ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                    } else {
                        return isset($decoded['loai_dl']) &&
                        (int)$decoded['nam'] === $year &&
                        (int)$decoded['quy'] === $period - 1 &&
                        ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                    }
                });
                if ($execute->isNotEmpty() && $adjacent->isNotEmpty()) {
                    $type_reports[] = 'Báo cáo kỳ thực hiện với liền kề';
                }

                //luỹ kế
            }
            else if ($typePeriod == 'month') {
                //xác định tồn tại thực hiện/kế hoạch
                $execute = $data->filter(function ($item) use ($year, $month) {
                    $decoded = json_decode($item, true);
                    return isset($decoded['loai_dl']) &&
                    $decoded['nam'] === $year &&
                    $decoded['thang'] === $month &&
                    ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                });
                $plan = $data->filter(function ($item) use ($year, $month) {
                    $decoded = json_decode($item, true);
                    return isset($decoded['loai_dl']) &&
                    $decoded['nam'] === $year &&
                    $decoded['thang'] === $month &&
                    $decoded['loai_dl'] === '1';
                });
                if ($execute->isNotEmpty() && ($plan->isNotEmpty() || $dataOther->isNotEmpty())) {
                    $type_reports[] = 'Báo cáo kỳ thực hiện với số kế hoạch';
                }

                //xác định tồn tại thực hiện/thực hiện cùng kỳ
                $executeSamePeriod = $data->filter(function ($item) use ($year, $month) {
                    $decoded = json_decode($item, true);
                    return isset($decoded['loai_dl']) &&
                    (int)$decoded['nam'] === $year - 1 &&
                    $decoded['thang'] === $month &&
                    ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                });
                if ($execute->isNotEmpty() && $executeSamePeriod->isNotEmpty()) {
                    $type_reports[] = 'Báo cáo kỳ thực hiện với cùng kỳ';
                }

                //xác định tồn tại thực hiện/ liền kề
                $adjacent = $data->filter(function ($item) use ($year, $month) {
                    $decoded = json_decode($item, true);
                    if($month == '01'){
                        return isset($decoded['loai_dl']) &&
                        (int)$decoded['nam'] === $year - 1 &&
                        $decoded['thang'] === '12' &&
                        ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                    } else {
                        return isset($decoded['loai_dl']) &&
                        $decoded['nam'] === $year &&
                        (int)$decoded['thang'] === $month - 1 &&
                        ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                    }
                });
                if ($execute->isNotEmpty() && $adjacent->isNotEmpty()) {
                    $type_reports[] = 'Báo cáo kỳ thực hiện với liền kề';
                }
            }
            else {
                //xác định tồn tại thực hiện/kế hoạch
                $execute = $data->filter(function ($item) use ($year) {
                    $decoded = json_decode($item, true);
                    return isset($decoded['loai_dl']) &&
                    $decoded['nam'] === $year &&
                    ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                });
                $plan = $data->filter(function ($item) use ($year) {
                    $decoded = json_decode($item, true);
                    return isset($decoded['loai_dl']) &&
                    $decoded['nam'] === $year &&
                    $decoded['loai_dl'] === '1';
                });
                if ($execute->isNotEmpty() && ($plan->isNotEmpty() || $dataOther->isNotEmpty())) {
                    $type_reports[] = 'Báo cáo kỳ thực hiện với số kế hoạch';
                }

                //xác định tồn tại thực hiện/thực hiện cùng kỳ
                $executeSamePeriod = $data->filter(function ($item) use ($year) {
                    $decoded = json_decode($item, true);
                    return isset($decoded['loai_dl']) &&
                    (int)$decoded['nam'] === $year - 1 &&
                    ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                });
                if ($execute->isNotEmpty() && $executeSamePeriod->isNotEmpty()) {
                    $type_reports[] = 'Báo cáo kỳ thực hiện với cùng kỳ';
                }

                //xác định tồn tại thực hiện/ liền kề
                $adjacent = $data->filter(function ($item) use ($year, $typePeriod) {
                    $decoded = json_decode($item, true);
                    if($typePeriod == '9-fist-month' || 'year'){
                        return isset($decoded['loai_dl']) &&
                        (int)$decoded['nam'] === $year - 1 &&
                        ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                    } else if ($typePeriod == '6-first-month') {
                        return isset($decoded['loai_dl']) &&
                        (int)$decoded['nam'] === $year -1 &&
                        (int)$decoded['ky_bc'] === '6-last-month' &&
                        ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                    } else {
                        return isset($decoded['loai_dl']) &&
                        (int)$decoded['nam'] === $year &&
                        (int)$decoded['ky_bc'] === '6-first-month' &&
                        ($decoded['loai_dl'] === '3' || $decoded['loai_dl'] === '4');
                    }
                });
                if ($execute->isNotEmpty() && $adjacent->isNotEmpty()) {
                    $type_reports[] = 'Báo cáo kỳ thực hiện với liền kề';
                }
            }


            $names = $data->map(function ($item) {
                $decoded = json_decode($item, true); // Giải mã trực tiếp mỗi phần tử
                return [
                    'thang' => $decoded['thang'] ?? null,
                    'quy' => $decoded['quy'] ?? null,
                    'ky_bc' => $decoded['ky_bc'] ?? null,
                    'nam' => $decoded['nam'] ?? null,
                    'loai_dl' => $decoded['loai_dl'] ?? null,
                    'thang' => $decoded['thang'] ?? null
                ];
            });
            return response()->json([
                'success' => true,
                'type_reports' => $type_reports,
                'yeah' => $year,
                'period' => $typePeriod,
                'data' => $names,

            ]);
        } catch(Exception $e)
    {
            abort(500);
        }
    }
public function getListCodes(Request $request)
    {
        try {
            $codes = DB::table('khoan_muc')->get();
            $nameCodes = $codes->map(function ($item) {
                $decoded = json_decode($item, true); // Giải mã trực tiếp mỗi phần tử
                return [
                    'name' => $decoded['name'] ?? null,
                ];
            });
            return response()->json([
                'success' => true,
                'listCodes' => $nameCodes
            ]);
        } catch (Exception $e) {
            abort(500);
        }
    }

    public function showReportcomparative(Request $request) {}

    public function getNameRequirementTH(Request $request)
    {
        $year = $request['year'];
        $typePeriod = $request['typePeriod'];
        $period = $request['period'] ?? null;
        $month = $request['month'] ?? null;
        if ($typePeriod == 'month') {
            $data = DB::table('process_requests')
                ->where('application_id', 73)
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.thang")) = ?', [$month])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [$year])
                ->pluck('data');
        } else if ($typePeriod == 'quarter') {
            $data = DB::table('process_requests')
                ->where('application_id', 73)
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.quy")) = ?', [$period])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [$year])
                ->pluck('data');
        } else {
            $data = DB::table('process_requests')
                ->where('application_id', 73)
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [$year])
                ->pluck('data');
        }
        //nếu có N3
        $nameRequirement = $data->filter(function ($item) {
            $decoded = json_decode($item, true);
            if ($decoded['ktth_vtg_pd'] == 1) {
                return isset($decoded['loai_dl']) &&
                    $decoded['ktth_vtg_pd'] == 1 &&
                    $decoded['loai_dl'] == 3;
            } else {
                return isset($decoded['loai_dl']) &&
                    $decoded['loai_dl'] == 3;
            }
        });
        //ko có thì kiếm N25
        if ($nameRequirement->isEmpty()) {
            $nameRequirement = $data->filter(function ($item) {
                $decoded = json_decode($item, true);
                if ($decoded['ktth_vtg_pd'] == 1) {
                    return isset($decoded['loai_dl']) &&
                        $decoded['ktth_vtg_pd'] == 1 &&
                        $decoded['loai_dl'] == 4;
                } else {
                    return isset($decoded['loai_dl']) &&
                        $decoded['loai_dl'] == 4;
                }
            });
        }
        if ($nameRequirement->isEmpty()) {
            return response()->json([
                'success' => true,
                'nameRequirementTH' => 'no report requirement for the selected reporting period.',
            ]);
        }
        $names = $nameRequirement->map(function ($item) {
            $decoded = json_decode($item, true); // Giải mã trực tiếp mỗi phần tử
            return $decoded['name'] ?? null;
        });
        return response()->json([
            'success' => true,
            'nameRequirementTH' => $names
        ]);
    }

    public function getNameRequirementKH(Request $request)
    {
        $year = $request['year'];
        $typePeriod = $request['typePeriod'];
        $period = $request['period'] ?? null;
        $month = $request['month'] ?? null;
        if ($typePeriod == 'month') {
            $data = DB::table('process_requests')
                ->where('application_id', 73)
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.thang")) = ?', [$month])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [$year])
                ->pluck('data');
        } else if ($typePeriod == 'quarter') {
            $data = DB::table('process_requests')
                ->where('application_id', 73)
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.quy")) = ?', [$period])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [$year])
                ->pluck('data');
        } else {
            $data = DB::table('process_requests')
                ->where('application_id', 73)
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [$year])
                ->pluck('data');
        }
        //nếu có N3
        $nameRequirement = $data->filter(function ($item) {
            $decoded = json_decode($item, true);
            if ($decoded['ktth_vtg_pd'] == 1) {
                return isset($decoded['loai_dl']) &&
                    $decoded['ktth_vtg_pd'] == 1 &&
                    $decoded['loai_dl'] == 1;
            } else {
                return isset($decoded['loai_dl']) &&
                    $decoded['loai_dl'] == 1;
            }
        });

        if ($typePeriod == "month") {
            $dataOther = DB::table('reports_import')
                ->where('report_year', $year)
                ->where('type_period ', $typePeriod)
                ->where('month ', $month);
        } else if ($typePeriod == "quarter") {
            $dataOther = DB::table('reports_import')
                ->where('report_year', $year)
                ->where('type_period ', $typePeriod)
                ->where('quarter ', $period);
        } else {
            $dataOther = DB::table('reports_import')
                ->where('report_year', $year)
                ->where('type_period ', $typePeriod);
        }


        if ($nameRequirement->isEmpty() && $dataOther->isEmpty()) {
            return response()->json([
                'success' => true,
                'nameRequirementTH' => 'no report requirement for the selected reporting period.',
            ]);
        }
        $names[] = $nameRequirement->map(function ($item) {
            $decoded = json_decode($item, true); // Giải mã trực tiếp mỗi phần tử
            return $decoded['name'] ?? null;
        });
        $name[] = $dataOther['name'];
        return response()->json([
            'success' => true,
            'nameRequirementTH' => $names
        ]);
    }

    public function getNameRequirementTHSamePeriod(Request $request)
    {
        $year = $request['year'];
        $typePeriod = $request['typePeriod'];
        $period = $request['period'] ?? null;
        $month = $request['month'] ?? null;
        if ($typePeriod == 'month') {
            $data = DB::table('process_requests')
                ->where('application_id', 73)
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.thang")) = ?', [$month])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [(int)($year - 1)])
                ->pluck('data');
        } else if ($typePeriod == 'quarter') {
            $data = DB::table('process_requests')
                ->where('application_id', 73)
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.quy")) = ?', [$period])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [(int)($year - 1)])
                ->pluck('data');
        } else {
            $data = DB::table('process_requests')
                ->where('application_id', 73)
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [(int)($year - 1)])
                ->pluck('data');
        }
        //nếu có N3
        $nameRequirement = $data->filter(function ($item) {
            $decoded = json_decode($item, true);
            if ($decoded['ktth_vtg_pd'] == 1) {
                return isset($decoded['loai_dl']) &&
                    $decoded['ktth_vtg_pd'] == 1 &&
                    $decoded['loai_dl'] == 3;
            } else {
                return isset($decoded['loai_dl']) &&
                    $decoded['loai_dl'] == 3;
            }
        });
        //ko có thì kiếm N25
        if ($nameRequirement->isEmpty()) {
            $nameRequirement = $data->filter(function ($item) {
                $decoded = json_decode($item, true);
                if ($decoded['ktth_vtg_pd'] == 1) {
                    return isset($decoded['loai_dl']) &&
                        $decoded['ktth_vtg_pd'] == 1 &&
                        $decoded['loai_dl'] == 4;
                } else {
                    return isset($decoded['loai_dl']) &&
                        $decoded['loai_dl'] == 4;
                }
            });
        }
        if ($nameRequirement->isEmpty()) {
            return response()->json([
                'success' => true,
                'nameRequirementTH' => 'no report requirement for the selected reporting period.',
            ]);
        }
        $names = $nameRequirement->map(function ($item) {
            $decoded = json_decode($item, true); // Giải mã trực tiếp mỗi phần tử
            return $decoded['name'] ?? null;
        });
        return response()->json([
            'success' => true,
            'nameRequirementTH' => $names
        ]);
    }

    public function getNameRequirementTHAdjacent(Request $request)
    {
        $year = $request['year'];
        $typePeriod = $request['typePeriod'];
        $period = $request['period'] ?? null;
        $month = $request['month'] ?? null;
        $data = DB::table('process_requests')
            ->where('application_id', 73)
            ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
            ->pluck('data');
        if ($typePeriod == 'month') {
            if ($month == '01') {
                //nếu có N3
                $nameRequirement = $data->filter(function ($item) use ($year, $month) {
                    $decoded = json_decode($item, true);
                    if ($decoded['ktth_vtg_pd'] == 1) {
                        return isset($decoded['loai_dl']) &&
                            (int)$decoded['nam'] == $year - 1 &&
                            $decoded['thang'] == 4 &&
                            $decoded['ktth_vtg_pd'] == 1 &&
                            $decoded['loai_dl'] == 3;
                    } else {
                        return isset($decoded['loai_dl']) &&
                            (int)$decoded['nam'] == $year - 1 &&
                            $decoded['thang'] == 12 &&
                            $decoded['loai_dl'] == 3;
                    }
                });
                //ko có thì kiếm N25
                if ($nameRequirement->isEmpty()) {
                    $nameRequirement = $data->filter(function ($item) use ($year) {
                        $decoded = json_decode($item, true);
                        if ($decoded['ktth_vtg_pd'] == 1) {
                            return isset($decoded['loai_dl']) &&
                                (int)$decoded['nam'] == $year - 1 &&
                                $decoded['thang'] == 12 &&
                                $decoded['ktth_vtg_pd'] == 1 &&
                                $decoded['loai_dl'] == 4;
                        } else {
                            return isset($decoded['loai_dl']) &&
                                (int)$decoded['nam'] == $year - 1 &&
                                $decoded['thang'] == 12 &&
                                $decoded['loai_dl'] == 4;
                        }
                    });
                }
            } else {
                //nếu có N3
                $nameRequirement = $data->filter(function ($item) use ($year, $month) {
                    $decoded = json_decode($item, true);
                    if ($decoded['ktth_vtg_pd'] == 1) {
                        return isset($decoded['loai_dl']) &&
                            $decoded['nam'] == $year &&
                            (int)$decoded['thang'] == $month - 1 &&
                            $decoded['ktth_vtg_pd'] == 1 &&
                            $decoded['loai_dl'] == 3;
                    } else {
                        return isset($decoded['loai_dl']) &&
                            $decoded['nam'] == $year &&
                            (int)$decoded['thang'] == $month - 1 &&
                            $decoded['loai_dl'] == 3;
                    }
                });
                //ko có thì kiếm N25
                if ($nameRequirement->isEmpty()) {
                    $nameRequirement = $data->filter(function ($item) use ($year) {
                        $decoded = json_decode($item, true);
                        if ($decoded['ktth_vtg_pd'] == 1) {
                            return isset($decoded['loai_dl']) &&
                                $decoded['nam'] == $year &&
                                (int)$decoded['thang'] == $month - 1 &&
                                $decoded['ktth_vtg_pd'] == 1 &&
                                $decoded['loai_dl'] == 4;
                        } else {
                            return isset($decoded['loai_dl']) &&
                                $decoded['nam'] == $year &&
                                (int)$decoded['thang'] == $month - 1 &&
                                $decoded['loai_dl'] == 4;
                        }
                    });
                }
            }
        } else if ($typePeriod == 'quarter') {
            if ($period == '1') {
                //nếu có N3
                $nameRequirement = $data->filter(function ($item) use ($year, $month) {
                    $decoded = json_decode($item, true);
                    if ($decoded['ktth_vtg_pd'] == 1) {
                        return isset($decoded['loai_dl']) &&
                            (int)$decoded['nam'] == $year - 1 &&
                            $decoded['quy'] == 4 &&
                            $decoded['ktth_vtg_pd'] == 1 &&
                            $decoded['loai_dl'] == 3;
                    } else {
                        return isset($decoded['loai_dl']) &&
                            (int)$decoded['nam'] == $year - 1 &&
                            $decoded['quy'] == 4 &&
                            $decoded['loai_dl'] == 3;
                    }
                });
                //ko có thì kiếm N25
                if ($nameRequirement->isEmpty()) {
                    $nameRequirement = $data->filter(function ($item) use ($year) {
                        $decoded = json_decode($item, true);
                        if ($decoded['ktth_vtg_pd'] == 1) {
                            return isset($decoded['loai_dl']) &&
                                (int)$decoded['nam'] == $year - 1 &&
                                $decoded['quy'] == 4 &&
                                $decoded['ktth_vtg_pd'] == 1 &&
                                $decoded['loai_dl'] == 4;
                        } else {
                            return isset($decoded['loai_dl']) &&
                                (int)$decoded['nam'] == $year - 1 &&
                                $decoded['quy'] == 4 &&
                                $decoded['loai_dl'] == 4;
                        }
                    });
                }
            } else {
                //nếu có N3
                $nameRequirement = $data->filter(function ($item) use ($year, $period) {
                    $decoded = json_decode($item, true);
                    if ($decoded['ktth_vtg_pd'] == 1) {
                        return isset($decoded['loai_dl']) &&
                            $decoded['nam'] == $year &&
                            (int)$decoded['quy'] == $period - 1 &&
                            $decoded['ktth_vtg_pd'] == 1 &&
                            $decoded['loai_dl'] == 3;
                    } else {
                        return isset($decoded['loai_dl']) &&
                            $decoded['nam'] == $year &&
                            (int)$decoded['quy'] == $period - 1 &&
                            $decoded['loai_dl'] == 3;
                    }
                });
                //ko có thì kiếm N25
                if ($nameRequirement->isEmpty()) {
                    $nameRequirement = $data->filter(function ($item) use ($year, $period) {
                        $decoded = json_decode($item, true);
                        if ($decoded['ktth_vtg_pd'] == 1) {
                            return isset($decoded['loai_dl']) &&
                                $decoded['nam'] == $year &&
                                (int)$decoded['quy'] == $period - 1 &&
                                $decoded['ktth_vtg_pd'] == 1 &&
                                $decoded['loai_dl'] == 4;
                        } else {
                            return isset($decoded['loai_dl']) &&
                                $decoded['nam'] == $year &&
                                (int)$decoded['quy'] == $month - 1 &&
                                $decoded['loai_dl'] == 4;
                        }
                    });
                }
            }
        } else {
            if ($typePeriod == '6-last-month') {
                $dataNew = DB::table('process_requests')
                    ->where('application_id', 73)
                    ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', ['6-first-month'])
                    ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [$year])
                    ->pluck('data');
                //nếu có N3
                $nameRequirement = $dataNew->filter(function ($item) {
                    $decoded = json_decode($item, true);
                    if ($decoded['ktth_vtg_pd'] == 1) {
                        return isset($decoded['loai_dl']) &&
                            $decoded['ktth_vtg_pd'] == 1 &&
                            $decoded['loai_dl'] == 3;
                    } else {
                        return isset($decoded['loai_dl']) &&
                            $decoded['loai_dl'] == 3;
                    }
                });
                //ko có thì kiếm N25
                if ($nameRequirement->isEmpty()) {
                    $nameRequirement = $data->filter(function ($item) {
                        $decoded = json_decode($item, true);
                        if ($decoded['ktth_vtg_pd'] == 1) {
                            return isset($decoded['loai_dl']) &&
                                $decoded['ktth_vtg_pd'] == 1 &&
                                $decoded['loai_dl'] == 4;
                        } else {
                            return isset($decoded['loai_dl']) &&
                                $decoded['loai_dl'] == 4;
                        }
                    });
                }
            } else {
                if ($typePeriod == '6-first-month') {
                    $dataNew = DB::table('process_requests')
                        ->where('application_id', 73)
                        ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', ['6-last-month'])
                        ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [(int)($year - 1)])
                        ->pluck('data');
                } else {
                    $dataNew = DB::table('process_requests')
                        ->where('application_id', 73)
                        ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.ky_bc")) = ?', [$typePeriod])
                        ->whereRaw('JSON_UNQUOTE(JSON_EXTRACT(data, "$.nam")) = ?', [(int)($year - 1)])
                        ->pluck('data');
                }

                //nếu có N3
                $nameRequirement = $dataNew->filter(function ($item) {
                    $decoded = json_decode($item, true);
                    if ($decoded['ktth_vtg_pd'] == 1) {
                        return isset($decoded['loai_dl']) &&
                            $decoded['ktth_vtg_pd'] == 1 &&
                            $decoded['loai_dl'] == 3;
                    } else {
                        return isset($decoded['loai_dl']) &&
                            $decoded['loai_dl'] == 3;
                    }
                });
                //ko có thì kiếm N25
                if ($nameRequirement->isEmpty()) {
                    $nameRequirement = $data->filter(function ($item) {
                        $decoded = json_decode($item, true);
                        if ($decoded['ktth_vtg_pd'] == 1) {
                            return isset($decoded['loai_dl']) &&
                                $decoded['ktth_vtg_pd'] == 1 &&
                                $decoded['loai_dl'] == 4;
                        } else {
                            return isset($decoded['loai_dl']) &&
                                $decoded['loai_dl'] == 4;
                        }
                    });
                }
            }
        }

        if ($nameRequirement->isEmpty()) {
            return response()->json([
                'success' => true,
                'nameRequirementTH' => 'no report requirement for the selected reporting period.',
            ]);
        }
        $names = $nameRequirement->map(function ($item) {
            $decoded = json_decode($item, true); // Giải mã trực tiếp mỗi phần tử
            return $decoded['name'] ?? null;
        });
        return response()->json([
            'success' => true,
            'nameRequirementTH' => $names
        ]);
    }
