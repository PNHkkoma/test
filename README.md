<?php
function _getChild($vid, $parent) {
  $GetChild = taxonomy_get_tree($vid, $parent, 1);
  $data = array();
  foreach($GetChild as $key => $rs) {
    $data[$key]->id = $rs->tid;
    $data[$key]->name = $rs->name;
    $data[$key]->children = _getChild($vid, $rs->tid);
  }
  return $data;
}

/**
 * Function for custom ajax
 */
function custom_api() {
  $return = array();
  if(empty($_POST)) {
    $_POST = json_decode(file_get_contents('php://input'), true); //lấy dữ liệu người dùng thông qua luồng php://input
    //Luồng php://input cho phép truy cập dữ liệu gửi lên từ phía client dưới dạng chuỗi dữ liệu nguyên thủy (raw data).
    //Hàm json_decode được sử dụng để giải mã chuỗi JSON thành một mảng PHP.
    //Tham số thứ hai của json_decode là true, cho phép kết quả trả về là một mảng
  }
  $type = isset($_POST['type']) ? $_POST['type'] : ""; //gán giá trị cho $type, isset là kiểm tra có rỗng ko

  //watchdog('lesson_xr', 'cApi call to %formly', array('%formly' => $type), WATCHDOG_NOTICE, $link = NULL);
  //return $type;
  if($type == "") {
    return _showMessage_api(400, "Không tồn tại loại api này", NULL);
  }
  switch($type) {
    case "GetTypeLocation":
      $allCategories = taxonomy_get_tree(2, 0, 1); //tạo cây từ taxonomy: 2 có nghĩa là id của taxonomy; 0 có nghĩa là id term nếu là 0 thì tạo cho toàn bộ vocabulary nên id thực tế sẽ -1 so với ở đây;1 là Số cấp độ của cây cần trả về. Để lại NULL để trả về tất cả các cấp độ.
      //thực tế ở đây trong vocabulary type palce hoặc category thì chưa có cha nào, sau khi getchild thì mới lấy con, khi đó sẽ rõ cha của nó là ai
      //và vấn đề là ta return ra data chứ ko return allcategories, tức ta cần return 1 mảng ấy
      $data = array();
      foreach($allCategories as $key => $rs) {
        $data[$key]->id = $rs->tid;
        $data[$key]->name = $rs->name;
        $data[$key]->children = _getChild(2, $rs->tid); //tạo và lấy cây con
        //cái này ứng với việc taxonomy_get_tree có số 1 thay vì null, nếu là null thì term con sẽ trả 2 lần trong cả getchild và $data, tức là trường hợp của mình 1 location có thể chứa 1 hoặc nhiều loaction nhỏ hơn ở bên trong nên làm vậy
      }
      return _showMessage_api(200, "Get category thành công ", $data);
      break;
    case "GetLocationInfoById":
      $locationID = $_POST['locationId'];
      $result = views_get_view_result('nodefunction', 'getlocationinfobyid', $locationID); //lấy ra thông tin view
      $data = new stdClass();
      foreach($result as $key => $rs) {
        $nid = $rs->nid;
        $node = node_load($nid);
        $data->id = $node->field_location_id['und'][0]['value'];
        $data->blockID = node_load($node->field_3d_space['und'][0]['nid'])->field_sessionid['und'][0]['value'];
        $data->name = $node->title;
        $data->location = $node->field_floor['und'][0]['value'];
        $data->category->cid = $node->field_category['und'][0]['tid'];
        $data->category->name = taxonomy_term_load($node->field_category['und'][0]['tid'])->name;
        $data->type->cid = $node->field_type_space['und'][0]['tid'];
        $data->type->name = taxonomy_term_load($node->field_type_space['und'][0]['tid'])->name;
        $data->description = $node->body['und'][0]['value'];
        $data->phoneNumber = $node->field_phone['und'][0]['value'];
        $data->openingTime = $node->field_opening_time['und'][0]['value'];
        $data->promotion = $node->field_khuyen_mai['und'][0]['value'];
        $data->logoUrl = $node->field_image_link['und'][0]['value'];
        $data->storeImageLink = $node->field_store_image['und'][0]['value'];
      }
      return _showMessage_api(200, "Thành công", $data);
      break;

    case "GetLocationInfomation":
      $SessionID = $_POST['BlockID'];
      $typeID = isset($_POST['TypeID']) ? $_POST['TypeID'] : "";
      //getlocationinfoblockid
      if($typeID == "")
        $result = views_get_view_result('nodefunction', 'getlocationinfoblockid', $SessionID);
      else
        $result = views_get_view_result('nodefunction', 'getlocationinfoblockid', $SessionID, $typeID);
      $data = array();
      foreach($result as $key => $rs) {
        $nid = $rs->nid;
        $node = node_load($nid);
        $data[$key]->id = $node->field_location_id['und'][0]['value'];
        $data[$key]->blockID = $SessionID;
        $data[$key]->name = $node->title;
        $data[$key]->location = $node->field_floor['und'][0]['value'];
        $data[$key]->category->cid = $node->field_category['und'][0]['tid'];
        $data[$key]->category->name = taxonomy_term_load($node->field_category['und'][0]['tid'])->name;
        $data[$key]->type->cid = $node->field_type_space['und'][0]['tid'];
        $data[$key]->type->name = taxonomy_term_load($node->field_type_space['und'][0]['tid'])->name;

        $data[$key]->logoUrl = $node->field_image_link['und'][0]['value'];
      }
      return _showMessage_api(200, "Thành công", $data);
      break;
    case "SearchStores":
      $_GET['title'] = $_POST['query'];
      $result = views_get_view_result('nodefunction', 'getlocationinfosearch');
      $data = array();
      foreach($result as $key => $rs) {
        $nid = $rs->nid;
        $node = node_load($nid);
        $data[$key]->id = $node->field_location_id['und'][0]['value'];
        $data[$key]->name = $node->title;
        $data[$key]->location = $node->field_floor['und'][0]['value'];
        $data[$key]->category->cid = $node->field_category['und'][0]['tid'];
        $data[$key]->category->name = taxonomy_term_load($node->field_category['und'][0]['tid'])->name;
        $data[$key]->type->cid = $node->field_type_space['und'][0]['tid'];
        $data[$key]->type->name = taxonomy_term_load($node->field_type_space['und'][0]['tid'])->name;
        $data[$key]->logoUrl = $node->field_image_link['und'][0]['value'];
      }
      return _showMessage_api(200, "Thành công", $data);
      break;
    case 'GetStoresByCategory':
      $cid = $_POST['category'];
      $SessionID = $_POST['BlockID'];
      $result = views_get_view_result('nodefunction', 'getlocationinfosearch', $cid, $blockId);
      $data = array();
      foreach($result as $key => $rs) {
        $nid = $rs->nid;
        $node = node_load($nid);
        if($node->)
        $data[$key]->id = $node->field_location_id['und'][0]['value'];
        $data[$key]->name = $node->title;
        $data[$key]->location = $node->field_floor['und'][0]['value'];
        $data[$key]->category->cid = $cid;
        $data[$key]->category->name = taxonomy_term_load($cid)->name;
        $data[$key]->type->cid = $node->field_type_space['und'][0]['tid'];
        $data[$key]->type->name = taxonomy_term_load($node->field_type_space['und'][0]['tid'])->name;
        $data[$key]->logoUrl = $node->field_image_link['und'][0]['value'];
      }
      return _showMessage_api(200, "Thành công", $data);
      break;
    case 'GetAllCategories':
      $allCategories = taxonomy_get_tree(3, 0, 1);
      $data = array();
      foreach($allCategories as $key => $rs) {
        $data[$key]->id = $rs->tid;
        $data[$key]->name = $rs->name;
        $data[$key]->children = _getChild(3, $rs->tid);
      }
      return _showMessage_api(200, "Get category thành công ", $data);
      break;
    case 'DeleteAnchoringTarget':
      $anchoringTargetId = $_POST['anchoringTargetId'];
      $getNodeData = views_get_view_result('nodefunction', 'getdynamicconent', $anchoringTargetId);
      if(count($getNodeData) > 0) {
        $nid = $getNodeData[0]->nid;
        //$node = node_load($nid);
        node_delete($nid);
        return _showMessage_api(200, "Xóa thành công AnchoringTarget ".$anchoringTargetId, NULL);
      }else{
        return _showMessage_api(400, "Không tồn tại AnchoringTarget này", NULL);
      }
      break;
    case 'GetBlockAnchoringTargetsData':
      $SessionID = $_POST['BlockID'];
      $SpaceGet = views_get_view_result('nodefunction', 'get3dspace', $SessionID);
      if(count($SpaceGet) > 0) {
        $spaceId = $SpaceGet[0]->nid;
        $dataList = new stdClass();
        //$dataList->id = $SessionID;
        $dataList->id = $SessionID;
        $dataList->targets = array();
        $getNodeData = views_get_view_result('nodefunction', 'getalldynamicconent', $spaceId);
        foreach($getNodeData as $key => $rs) {
          $node = node_load($rs->nid);
          $anchoringTargetData = new stdClass();
          $anchoringTargetData->id = $node->field_sessionid['und'][0]['value'];
          $anchoringTargetData->boundSize->x = $node->field_boundsize['und'][0]['value'];
          $anchoringTargetData->boundSize->y = $node->field_boundsize['und'][1]['value'];
          $anchoringTargetData->boundSize->z = $node->field_boundsize['und'][2]['value'];
          $anchoringTargetData->transform->orientation->w = $node->field_orientation2['und'][0]['value'];
          $anchoringTargetData->transform->orientation->x = $node->field_orientation2['und'][1]['value'];
          $anchoringTargetData->transform->orientation->y = $node->field_orientation2['und'][2]['value'];
          $anchoringTargetData->transform->orientation->z = $node->field_orientation2['und'][3]['value'];
          $anchoringTargetData->transform->position->x = $node->field_position2['und'][0]['value'];
          $anchoringTargetData->transform->position->y = $node->field_position2['und'][1]['value'];
          $anchoringTargetData->transform->position->z = $node->field_position2['und'][2]['value'];
          $anchoringTargetData->transform->scale->x = $node->field_scale2['und'][0]['value'];
          $anchoringTargetData->transform->scale->y = $node->field_scale2['und'][1]['value'];
          $anchoringTargetData->transform->scale->z = $node->field_scale2['und'][2]['value'];
          $anchoringTargetData->animation = $node->field_animation_['und'][0]['value'];
          $anchoringTargetData->media->name = $node->field_name['und'][0]['value'];
          $anchoringTargetData->media->url = $node->field_url['und'][0]['value'];
          $anchoringTargetData->media->Type = $node->field_type['und'][0]['value'];
          $anchoringTargetData->media->id = 0;
          $dataList->targets[$key] = $anchoringTargetData;
        }
        return _showMessage_api(200, "Tìm thấy ".count($getNodeData)." AnchoringTarget của ".$SessionID, $dataList);
      }else{
        return _showMessage_api(400, "Không tồn tại SessionID này", NULL);
      }
      break;
    case 'GetAnchoringTarget':
      $anchoringTargetId = $_POST['anchoringTargetId'];
      $getNodeData = views_get_view_result('nodefunction', 'getdynamicconent', $anchoringTargetId);
      if(count($getNodeData) > 0) {
        $nid = $getNodeData[0]->nid;
        $node = node_load($nid);
        $anchoringTargetData = new stdClass();
        $anchoringTargetData->id = $node->field_sessionid['und'][0]['value'];
        $anchoringTargetData->boundSize->x = $node->field_boundsize['und'][0]['value'];
        $anchoringTargetData->boundSize->y = $node->field_boundsize['und'][1]['value'];
        $anchoringTargetData->boundSize->z = $node->field_boundsize['und'][2]['value'];

        $anchoringTargetData->transform->orientation->w = $node->field_orientation2['und'][0]['value'];
        $anchoringTargetData->transform->orientation->x = $node->field_orientation2['und'][1]['value'];
        $anchoringTargetData->transform->orientation->y = $node->field_orientation2['und'][2]['value'];
        $anchoringTargetData->transform->orientation->z = $node->field_orientation2['und'][3]['value'];
        $anchoringTargetData->transform->position->x = $node->field_position2['und'][0]['value'];
        $anchoringTargetData->transform->position->y = $node->field_position2['und'][1]['value'];
        $anchoringTargetData->transform->position->z = $node->field_position2['und'][2]['value'];
        $anchoringTargetData->transform->scale->x = $node->field_scale2['und'][0]['value'];
        $anchoringTargetData->transform->scale->y = $node->field_scale2['und'][1]['value'];
        $anchoringTargetData->transform->scale->z = $node->field_scale2['und'][2]['value'];
        $anchoringTargetData->animation = $node->field_animation_['und'][0]['value'];
        $anchoringTargetData->media->name = $node->field_name['und'][0]['value'];
        $anchoringTargetData->media->url = $node->field_url['und'][0]['value'];
        $anchoringTargetData->media->Type = $node->field_type['und'][0]['value'];
        $anchoringTargetData->media->id = 0;
        return _showMessage_api(200, "Lấy thông tin thành công AnchoringTarget ".$anchoringTargetId, $anchoringTargetData);
      }else{
        return _showMessage_api(400, "Không tồn tại AnchoringTarget này", NULL);
      }
      break;
    case 'UpdateAnchoringTarget':
      $anchoringTargetId = $_POST['anchoringTargetId'];
      $anchoringTargetDataString = $_POST['anchoringTargetData'];
      watchdog('custom', 'Debug: %formly', array( '%formly' => $anchoringTargetDataString), WATCHDOG_ERROR, $link = NULL);
      $anchoringTargetData = json_decode($anchoringTargetDataString);
      if(!is_object($anchoringTargetData)) {
        return _showMessage_api(400, "Data truyền vào không đúng", NULL);
      }
      $getNodeData = views_get_view_result('nodefunction', 'getdynamicconent', $anchoringTargetId);
      if(count($getNodeData) > 0) {
        $nid = $getNodeData[0]->nid;
        $node = node_load($nid);
        $node->field_boundsize['und'][0]['value'] = $anchoringTargetData->boundSize->x;
        $node->field_boundsize['und'][1]['value'] = $anchoringTargetData->boundSize->y;
        $node->field_boundsize['und'][2]['value'] = $anchoringTargetData->boundSize->z;
        $node->field_orientation2['und'][0]['value'] = $anchoringTargetData->transform->orientation->w;
        $node->field_orientation2['und'][1]['value'] = $anchoringTargetData->transform->orientation->x;
        $node->field_orientation2['und'][2]['value'] = $anchoringTargetData->transform->orientation->y;
        $node->field_orientation2['und'][3]['value'] = $anchoringTargetData->transform->orientation->z;
        $node->field_position2['und'][0]['value'] = $anchoringTargetData->transform->position->x;
        $node->field_position2['und'][1]['value'] = $anchoringTargetData->transform->position->y;
        $node->field_position2['und'][2]['value'] = $anchoringTargetData->transform->position->z;
        $node->field_scale2['und'][0]['value'] = $anchoringTargetData->transform->scale->x;
        $node->field_scale2['und'][1]['value'] = $anchoringTargetData->transform->scale->y;
        $node->field_scale2['und'][2]['value'] = $anchoringTargetData->transform->scale->z;
        $node->field_animation_['und'][0]['value'] = $anchoringTargetData->animation;
        $node->field_name['und'][0]['value'] = $anchoringTargetData->media->name;
        $node->field_url['und'][0]['value'] = $anchoringTargetData->media->url;
        $node->field_type['und'][0]['value'] = $anchoringTargetData->media->Type;
        node_save($node);
        return _showMessage_api(200, "Cập nhật thành công AnchoringTarget ".$anchoringTargetId, $node);
      }else{
        return _showMessage_api(400, "Không tồn tại AnchoringTarget này", NULL);
      }

      break;
    case 'AddNewAnchoringTarget':
      $SessionID = $_POST['BlockID'];
      $anchoringTargetDataString = $_POST['anchoringTargetData'];
      watchdog('custom', 'Debug: %formly', array( '%formly' => $anchoringTargetDataString), WATCHDOG_ERROR, $link = NULL);
      $anchoringTargetData = json_decode($anchoringTargetDataString);
      if(!is_object($anchoringTargetData)) {
        return _showMessage_api(400, "Data truyền vào không đúng", NULL);
      }
      //Cap nhat neu da ton tai
      $getNodeData = views_get_view_result('nodefunction', 'getdynamicconent', $anchoringTargetData->id);
      if(count($getNodeData) > 0) {
        $nid = $getNodeData[0]->nid;
        $node = node_load($nid);
        $node->field_boundsize['und'][0]['value'] = $anchoringTargetData->boundSize->x;
        $node->field_boundsize['und'][1]['value'] = $anchoringTargetData->boundSize->y;
        $node->field_boundsize['und'][2]['value'] = $anchoringTargetData->boundSize->z;
        $node->field_orientation2['und'][0]['value'] = $anchoringTargetData->transform->orientation->w;
        $node->field_orientation2['und'][1]['value'] = $anchoringTargetData->transform->orientation->x;
        $node->field_orientation2['und'][2]['value'] = $anchoringTargetData->transform->orientation->y;
        $node->field_orientation2['und'][3]['value'] = $anchoringTargetData->transform->orientation->z;
        $node->field_position2['und'][0]['value'] = $anchoringTargetData->transform->position->x;
        $node->field_position2['und'][1]['value'] = $anchoringTargetData->transform->position->y;
        $node->field_position2['und'][2]['value'] = $anchoringTargetData->transform->position->z;
        $node->field_scale2['und'][0]['value'] = $anchoringTargetData->transform->scale->x;
        $node->field_scale2['und'][1]['value'] = $anchoringTargetData->transform->scale->y;
        $node->field_scale2['und'][2]['value'] = $anchoringTargetData->transform->scale->z;
        $node->field_animation_['und'][0]['value'] = $anchoringTargetData->animation;
        $node->field_name['und'][0]['value'] = $anchoringTargetData->media->name;
        $node->field_url['und'][0]['value'] = $anchoringTargetData->media->url;
        $node->field_type['und'][0]['value'] = $anchoringTargetData->media->Type;
        node_save($node);
        return _showMessage_api(200, "Cập nhật thành công AnchoringTarget ".$anchoringTargetData->id, $node);
      }
      //End

      $SpaceGet = views_get_view_result('nodefunction', 'get3dspace', $SessionID);
      if(count($SpaceGet) > 0) {
        $spaceId = $SpaceGet[0]->nid;
        $node = new stdClass();
        $node->type = "dynamic_content";
        $node->title = "Dynamic content ".strtotime("now");
        $node->language = LANGUAGE_NONE;
        $node->field_sessionid['und'][0]['value'] = $anchoringTargetData->id;
        $node->field_boundsize['und'][0]['value'] = $anchoringTargetData->boundSize->x;
        $node->field_boundsize['und'][1]['value'] = $anchoringTargetData->boundSize->y;
        $node->field_boundsize['und'][2]['value'] = $anchoringTargetData->boundSize->z;

        $node->field_orientation2['und'][0]['value'] = $anchoringTargetData->transform->orientation->w;
        $node->field_orientation2['und'][1]['value'] = $anchoringTargetData->transform->orientation->x;
        $node->field_orientation2['und'][2]['value'] = $anchoringTargetData->transform->orientation->y;
        $node->field_orientation2['und'][3]['value'] = $anchoringTargetData->transform->orientation->z;
        $node->field_position2['und'][0]['value'] = $anchoringTargetData->transform->position->x;
        $node->field_position2['und'][1]['value'] = $anchoringTargetData->transform->position->y;
        $node->field_position2['und'][2]['value'] = $anchoringTargetData->transform->position->z;
        $node->field_scale2['und'][0]['value'] = $anchoringTargetData->transform->scale->x;
        $node->field_scale2['und'][1]['value'] = $anchoringTargetData->transform->scale->y;
        $node->field_scale2['und'][2]['value'] = $anchoringTargetData->transform->scale->z;
        $node->field_animation_['und'][0]['value'] = $anchoringTargetData->animation;
        $node->field_name['und'][0]['value'] = $anchoringTargetData->media->name;
        $node->field_url['und'][0]['value'] = $anchoringTargetData->media->url;
        $node->field_type['und'][0]['value'] = $anchoringTargetData->media->Type;
        $node->field_3d_space['und'][0]['nid'] = $spaceId;
        node_object_prepare($node);
        $node->uid = 1;
        $node = node_submit($node);
        node_save($node);
        return _showMessage_api(200, "Tạo mới thành công AnchoringTarget ".$anchoringTargetData->id, $node);

      }else{
        return _showMessage_api(400, "Không tồn tại SessionID này", NULL);
      }
      break;
    case 'AddNavigationTarget':
      $blockId = $_POST['blockID'];
      $data = $_POST['data'];
      $data = json_decode($data);
      if(!is_object($data)) {
        return _showMessage_api(400, "Data truyền vào không đúng", NULL);
      }
      //Start update if isset
      $rs = views_get_view_result('nodefunction', 'getnavigationtarget2', $data->id);
      if(count($rs) > 0) {
        $node = node_load($rs[0]->nid);
        if($node) {
          $node->title = $data->name;
          $node->field_orientation2['und'][0]['value'] = $data->transform->orientation->w;
          $node->field_orientation2['und'][1]['value'] = $data->transform->orientation->x;
          $node->field_orientation2['und'][2]['value'] = $data->transform->orientation->y;
          $node->field_orientation2['und'][3]['value'] = $data->transform->orientation->z;
          $node->field_position2['und'][0]['value'] = $data->transform->position->x;
          $node->field_position2['und'][1]['value'] = $data->transform->position->y;
          $node->field_position2['und'][2]['value'] = $data->transform->position->z;
          $node->field_scale2['und'][0]['value'] = $data->transform->scale->x;
          $node->field_scale2['und'][1]['value'] = $data->transform->scale->y;
          $node->field_scale2['und'][2]['value'] = $data->transform->scale->z;
          node_save($node);
          return _showMessage_api(200, "Cập nhật thành công NavigationTarget ".$data->id, $node);
        }
      }
      //END update if isset
      $SpaceGet = views_get_view_result('nodefunction', 'get3dspace', $blockId);
      if(count($SpaceGet) > 0) {
        $spaceId = $SpaceGet[0]->nid;
        $node = new stdClass();
        $node->type = "navigation_target";
        $node->title = $data->name;
        $node->language = LANGUAGE_NONE;
        $node->field_id['und'][0]['value'] = $data->id;

        $node->field_orientation2['und'][0]['value'] = $data->transform->orientation->w;
        $node->field_orientation2['und'][1]['value'] = $data->transform->orientation->x;
        $node->field_orientation2['und'][2]['value'] = $data->transform->orientation->y;
        $node->field_orientation2['und'][3]['value'] = $data->transform->orientation->z;
        $node->field_position2['und'][0]['value'] = $data->transform->position->x;
        $node->field_position2['und'][1]['value'] = $data->transform->position->y;
        $node->field_position2['und'][2]['value'] = $data->transform->position->z;
        $node->field_scale2['und'][0]['value'] = $data->transform->scale->x;
        $node->field_scale2['und'][1]['value'] = $data->transform->scale->y;
        $node->field_scale2['und'][2]['value'] = $data->transform->scale->z;
        $node->field_3d_space['und'][0]['nid'] = $spaceId;
        $locationInfo = views_get_view_result('nodefunction', 'getlocationinfo', $data->locationID);
        if(count($locationInfo) > 0) {
          $node->field_location_info['und'][0]['nid'] = $locationInfo[0]->nid;
        }
        node_object_prepare($node);
        $node->uid = 1;
        $node = node_submit($node);
        node_save($node);
        return _showMessage_api(200, "Tạo mới thành công NavigationTarget ".$data->id, $node);
      }else{
        return _showMessage_api(400, "Không tồn tại BlockID này", NULL);
      }
      break;
    case 'UpdateNavigationTarget':
      $NavigationTargetID = $_POST['NavigationTargetID'];
      $data = $_POST['NavigationTargetData'];
      $data = json_decode($data);
      if(!is_object($data)) {
        return _showMessage_api(400, "Data truyền vào không đúng", NULL);
      }
      $rs = views_get_view_result('nodefunction', 'getnavigationtarget2', $NavigationTargetID);
      if(count($rs) > 0) {
        $node = node_load($rs[0]->nid);
        if($node) {
          $node->title = $data->name;
          $node->field_orientation2['und'][0]['value'] = $data->transform->orientation->w;
          $node->field_orientation2['und'][1]['value'] = $data->transform->orientation->x;
          $node->field_orientation2['und'][2]['value'] = $data->transform->orientation->y;
          $node->field_orientation2['und'][3]['value'] = $data->transform->orientation->z;
          $node->field_position2['und'][0]['value'] = $data->transform->position->x;
          $node->field_position2['und'][1]['value'] = $data->transform->position->y;
          $node->field_position2['und'][2]['value'] = $data->transform->position->z;
          $node->field_scale2['und'][0]['value'] = $data->transform->scale->x;
          $node->field_scale2['und'][1]['value'] = $data->transform->scale->y;
          $node->field_scale2['und'][2]['value'] = $data->transform->scale->z;
          node_save($node);
          return _showMessage_api(200, "Cập nhật thành công NavigationTarget ".$data->id, $node);
        }else{
          return _showMessage_api(400, "Không tồn tại NavigationTarget này", NULL);
        }

      }else{
        return _showMessage_api(400, "Không tồn tại NavigationTarget này", NULL);
      }
      break;
    case 'GetBlockNavigationTargetData':
      $navigationTargetID = isset($_POST['navigationTargetID']) ? $_POST['navigationTargetID'] : "";
      $blockId = $_POST['blockID'];
      if($navigationTargetID == "") {
        $rs = views_get_view_result('nodefunction', 'getnavigationtarget', $blockId);
        $dataList = new stdClass();
        $dataList->id = $blockId;
        $dataList->targets = array();
        foreach($rs as $key => $r) {
          $node = node_load($r->nid);
          $navigation_target = new stdClass();
          $navigation_target->id = $node->field_id['und'][0]['value'];
          $navigation_target->transform->orientation->w = $node->field_orientation2['und'][0]['value'];
          $navigation_target->transform->orientation->x = $node->field_orientation2['und'][1]['value'];
          $navigation_target->transform->orientation->y = $node->field_orientation2['und'][2]['value'];
          $navigation_target->transform->orientation->z = $node->field_orientation2['und'][3]['value'];
          $navigation_target->transform->position->x = $node->field_position2['und'][0]['value'];
          $navigation_target->transform->position->y = $node->field_position2['und'][1]['value'];
          $navigation_target->transform->position->z = $node->field_position2['und'][2]['value'];
          $navigation_target->transform->scale->x = $node->field_scale2['und'][0]['value'];
          $navigation_target->transform->scale->y = $node->field_scale2['und'][1]['value'];
          $navigation_target->transform->scale->z = $node->field_scale2['und'][2]['value'];
          $navigation_target->locationID = $r->field_field_location_id[0]['raw']['value'];
          $navigation_target->name = $node->title;
          $dataList->targets[] = $navigation_target;
        }
        return _showMessage_api(200, "Thành công ", $dataList);
      }else{
        $rs = views_get_view_result('nodefunction', 'getnavigationtarget', $blockId, $navigationTargetID);
        if(count($rs) > 0) {
          $node = node_load($rs[0]->nid);
          $navigation_target = new stdClass();
          $navigation_target->id = $node->field_id['und'][0]['value'];
          $navigation_target->transform->orientation->w = $node->field_orientation2['und'][0]['value'];
          $navigation_target->transform->orientation->x = $node->field_orientation2['und'][1]['value'];
          $navigation_target->transform->orientation->y = $node->field_orientation2['und'][2]['value'];
          $navigation_target->transform->orientation->z = $node->field_orientation2['und'][3]['value'];
          $navigation_target->transform->position->x = $node->field_position2['und'][0]['value'];
          $navigation_target->transform->position->y = $node->field_position2['und'][1]['value'];
          $navigation_target->transform->position->z = $node->field_position2['und'][2]['value'];
          $navigation_target->transform->scale->x = $node->field_scale2['und'][0]['value'];
          $navigation_target->transform->scale->y = $node->field_scale2['und'][1]['value'];
          $navigation_target->transform->scale->z = $node->field_scale2['und'][2]['value'];
          $navigation_target->locationID = $rs[0]->field_field_location_id[0]['raw']['value'];
          $navigation_target->name = $node->title;
          return _showMessage_api(200, "Thành công ", $navigation_target);
        }
      }

      return _showMessage_api(400, "Không tồn tại BlockID này", NULL);
      break;
    case "GetNavigationTargetData":
      $navigationTargetID = isset($_POST['NavigationTargetID']) ? $_POST['NavigationTargetID'] : "";
      $rs = views_get_view_result('nodefunction', 'getnavigationtarget2', $navigationTargetID);
      if(count($rs) > 0) {
        $node = node_load($rs[0]->nid);
        $navigation_target = new stdClass();
        $navigation_target->id = $node->field_id['und'][0]['value'];
        $navigation_target->transform->orientation->w = $node->field_orientation2['und'][0]['value'];
        $navigation_target->transform->orientation->x = $node->field_orientation2['und'][1]['value'];
        $navigation_target->transform->orientation->y = $node->field_orientation2['und'][2]['value'];
        $navigation_target->transform->orientation->z = $node->field_orientation2['und'][3]['value'];
        $navigation_target->transform->position->x = $node->field_position2['und'][0]['value'];
        $navigation_target->transform->position->y = $node->field_position2['und'][1]['value'];
        $navigation_target->transform->position->z = $node->field_position2['und'][2]['value'];
        $navigation_target->transform->scale->x = $node->field_scale2['und'][0]['value'];
        $navigation_target->transform->scale->y = $node->field_scale2['und'][1]['value'];
        $navigation_target->transform->scale->z = $node->field_scale2['und'][2]['value'];
        $navigation_target->locationID = $rs[0]->field_field_location_id[0]['raw']['value'];
        $navigation_target->name = $node->title;
        return _showMessage_api(200, "Thành công ", $navigation_target);
      }else{
        return _showMessage_api(400, "Không tồn tại NavigationTarget này", NULL);
      }
      break;
    case "DeleteNavigationTarget":
      $navigationTargetID = isset($_POST['NavigationTargetID']) ? $_POST['NavigationTargetID'] : "";
      $rs = views_get_view_result('nodefunction', 'getnavigationtarget2', $navigationTargetID);
      if(count($rs) > 0) {
        node_delete($rs[0]->nid);
        return _showMessage_api(200, "Xóa Thành công ", NULL);
      }else{
        return _showMessage_api(400, "Không tồn tại NavigationTarget này", NULL);
      }
      break;
  }
  drupal_json_output($return);
}


function _showMessage_api($statusCode, $message, $data = NULL) {
  $return['status'] = $statusCode;
  $return['message'] = $message;
  $return['data'] = $data;
  return drupal_json_output($return);
}
