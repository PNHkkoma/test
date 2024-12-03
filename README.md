SELECT
    bhn.index AS 'STT',
    km.name_vie AS 'Chỉ tiêu',
    km.name_eng AS 'List',
    km.code AS Code,
    bhn.vtg_dividend AS 'VTG(gồm cổ tức)',
    bhn.vtg_no_dividend AS 'VTG(không gồm cổ tức)',
    bhn.vtg_net AS 'VTG NET',
    bhn.vtg_net_dc AS 'Điều chỉnh nội bộ VTG và TT',
    bhn.dc_tt AS 'Điều chỉnh nội bộ các trung tâm',
    bhn.dc_cltg AS 'Đ/c PB CLTG',
    bhn.dc_khac AS 'Đ/c Khác',
    bhn.cong_ngang AS 'Cộng ngang',
    bhn.hop_nhat AS 'Hợp nhất',
    bhn.hop_nhat_vtp AS 'Hợp nhất + VTP',
    bhn.hop_nhat_tru_lo AS 'Hợp nhất loại trừ lỗ công ty liên kết vượt qua vốn góp',
    bhn.hop_nhat_vtp_tru_lo AS 'Hợp nhất + VTP loại trừ lỗ công ty liên kết vượt qua vốn góp',
    CASE
        WHEN bhn.company_id='VTC'
        THEN bhn.value
        ELSE NULL
    END AS 'VTC',
    CASE
        WHEN bhn.company_id='STL'
        THEN bhn.value
        ELSE NULL
    END AS 'STL',
    CASE
        WHEN bhn.company_id='NCM'
        THEN bhn.value
        ELSE NULL
    END AS 'NCM',
    CASE
        WHEN bhn.company_id='MVT'
        THEN bhn.value
        ELSE NULL
    END AS 'MVT',
    CASE
        WHEN bhn.company_id='VTL'
        THEN bhn.value
        ELSE NULL
    END AS 'VTL',
    CASE
        WHEN bhn.company_id='VCR'
        THEN bhn.value
        ELSE NULL
    END AS 'VCR',
    CASE
        WHEN bhn.company_id='VTB'
        THEN bhn.value
        ELSE NULL
    END AS 'VTB',
    CASE
        WHEN bhn.company_id='VTZ'
        THEN bhn.value
        ELSE NULL
    END AS 'VTZ',
    CASE
        WHEN bhn.company_id='NCM_E'
        THEN bhn.value
        ELSE NULL
    END AS 'NCM_E',
    CASE
        WHEN bhn.company_id='VTP'
        THEN bhn.value
        ELSE NULL
    END AS 'VTP',
    CASE
        WHEN bhn.company_id='MYN'
        THEN bhn.value
        ELSE NULL
    END AS 'MYN',
    CASE
        WHEN bhn.company_id='MOV_E'
        THEN bhn.value
        ELSE NULL
    END AS 'MOV_E',
    CASE
        WHEN bhn.company_id='VTL_E'
        THEN bhn.value
        ELSE NULL
    END AS 'VTL_E',
    CASE
        WHEN bhn.company_id='MYN_E'
        THEN bhn.value
        ELSE NULL
    END AS 'MYN_E',
    CASE
        WHEN bhn.company_id='VTC_E'
        THEN bhn.value
        ELSE NULL
    END AS 'VTC_E',
    CASE
        WHEN bhn.company_id='VTB_E'
        THEN bhn.value
        ELSE NULL
    END AS 'VTB_E',
    CASE
        WHEN bhn.company_id='STL_E'
        THEN bhn.value
        ELSE NULL
    END AS 'STL_E',
    CASE
        WHEN bhn.company_id='VTZ_E'
        THEN bhn.value
        ELSE NULL
    END AS 'VTZ_E',
    bhn.year,
    bhn.Report_id AS 'Request id'
FROM
    vtg_ke_hoach_khac bhn
    JOIN khoan_muc km ON bhn.code = km.code
GROUP BY
    km.name_vie,
    bhn.type_period,
    bhn.YEAR
    ORDER BY
    bhn.index
