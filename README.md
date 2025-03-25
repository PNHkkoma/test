itms-services://?action=download-manifest&url=https%3A%2F%2Fviettelfamily.com%2Fuploads%2Fviettel360%2Fvops%2Fios%2FvOps.plist

https://www.figma.com/design/UUhBgaK92cgYvvmLmcHmEo/QLH%C4%90_v3_%C4%91%C3%A1nh-s%E1%BB%91?m=auto&t=IndL3BmHleiFKCE0-6



https://www.figma.com/design/R8Hk8WcGLjn78KUDDnpHmj/UX_PVN?m=auto&t=UxmdAmGHfwE7tYQR-1
m=auto&t=UxmdAmGHfwE7tYQR-1
use Illuminate\Support\Facades\Storage;
use Maatwebsite\Excel\Facades\Excel;
use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;

public function handleExcelFile()
{
    // Retrieve file from MinIO
    $filePath = 'path/to/excel-file.xlsx';
    $tempFile = Storage::disk('s3')->get($filePath);


    <ng-template #cancelChangesModal let-modal>
    <div class="modal-wrapper">
        <div class="modal-header px-24 pt-24 pb-0">
            <span style="font-weight: 600; font-size: 20px;">{{'WARNINGS.UNSAVED_CHANGES' | translate}}</span>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                    (click)="modal.dismiss()">
            </button>
        </div>
        <div class="modal-body p-24">{{'WARNINGS.CANCEL_CHANGES_WARNING_TEXT' | translate}}</div>
        <div class="modal-footer d-flex align-items-start btns px-24 pt-0 pb-24">
            <button type="button" class="button cancel" (click)="modal.dismiss();" [autoFocus]="true">
                {{'VERBS.BACK' | translate}}
            </button>
            <button type="button" class="ms-2 button save" (click)=" this._router.navigate(['/cxsurvey/list'])">
                {{'WARNINGS.EXIT_WITHOUT_SAVING' | translate}}
            </button>
        </div>
    </div>
</ng-template>

    // Load the Excel content
    $spreadsheet = \PhpOffice\PhpSpreadsheet\IOFactory::loadFromString($tempFile);

    // Modify the content as needed
    $sheet = $spreadsheet->g
    $sheet->setCellValue('A1', 'Modified Content');

    // Save the modified file to a temporary location
    $writer = new Xlsx($spreadsheet);
    $tempPath = storage_path('app/temp-file.xlsx');
    $writer->save($tempPath);

    // Return the modified file for download
    return response()->download($tempPath)-
    
    
    
    
    >deleteFileAfterSend(true);
}





https://id.tableau.com/token/825a6830a5b04f5abe10e0d065b0447d
