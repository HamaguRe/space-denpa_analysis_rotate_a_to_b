// 特異点近傍の計算精度を確認する

use std::fs;
use std::io::{Write, BufWriter};
use quaternion_core as quat;
use quat::{Vector3, Quaternion};

const OUT_FILE_PATH: &'static str = "./result.csv";

fn main() {
    // 計算結果の保存先（同一ファイルが存在したら上書き）
    let mut file = BufWriter::new(fs::File::create(OUT_FILE_PATH).unwrap());

    let a = [-0.5, -1.5, 2.8];

    let (range, resolution) = (0..64000, 0.0001);  // 全域
    //let (range, resolution) = (31390000..31450000, 0.0000001);  // θ=π近傍
    //let (range, resolution) = (62800000..62860000, 0.0000001);  // θ=2π近傍
    //let (range, resolution) = (31415750..31416100, 0.0000001);  // θ=π近傍（より拡大して見る）
    for i in range {
        let angle = i as f32 * resolution;

        // 特異点を通るようにする
        let axis = orthogonal_vector(a);
        let q = quat::from_axis_angle(axis, angle);
        let b = quat::point_rotation(q, a);

        // 従来のアルゴリズム（特異点あり）
        let q_old = rotate_a_to_b_old(a, b);

        // 新しいアルゴリズム（特異点なし）
        let q_new = rotate_a_to_b_new(a, b);

        let b_old = quat::point_rotation(q_old, a);
        let b_new = quat::point_rotation(q_new, a);
        let error_old = quat::sub(b, b_old);
        let error_new = quat::sub(b, b_new);
        file.write(format!(
            "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n",
            angle,
            q.0, q.1[0], q.1[1], q.1[2],
            q_old.0, q_old.1[0], q_old.1[1], q_old.1[2],
            q_new.0, q_new.1[0], q_new.1[1], q_new.1[2],
            b[0], b[1], b[2],
            b_old[0], b_old[1], b_old[2],
            b_new[0], b_new[1], b_new[2],
            error_old[0], error_old[1], error_old[2],
            error_new[0], error_new[1], error_new[2]
        ).as_bytes()).unwrap();
    }
    println!("Result has been saved to {}", OUT_FILE_PATH);
}

/// 従来のアルゴリズム（特異点がある）
fn rotate_a_to_b_old(a: Vector3<f32>, b: Vector3<f32>) -> Quaternion<f32> {
    let norm_a = quat::norm(a);
    let norm_b = quat::norm(b);
    let mut tmp = quat::dot(a, b) / (norm_a * norm_b);
    tmp = if tmp.abs() > 1.0 {1.0f32.copysign(tmp)} else {tmp};
    let theta = tmp.acos();
    let a_cross_b = quat::cross(a, b);
    let norm_a_cross_b_inv = quat::norm(a_cross_b).recip();
    if norm_a_cross_b_inv.is_finite() {
        let (sin, cos) = (theta * 0.5).sin_cos();
        (cos, quat::scale(sin * norm_a_cross_b_inv, a_cross_b))
    } else {
        if quat::dot(a, b).is_sign_positive() {
            (1.0, [0.0; 3])              // theta==0のとき
        } else {
            (0.0, orthogonal_vector(a))  // theta==πのとき
        }
    }
}

/// 特異点を持たない求解アルゴリズム
fn rotate_a_to_b_new(a: Vector3<f32>, b: Vector3<f32>) -> Quaternion<f32> {
    let a_u = quat::normalize(a);
    let b_u = quat::normalize(b);

    if quat::dot(a_u, b_u) > 0.0 {
        let axis = quat::add(a_u, b_u);
        let norm_inv = quat::norm(axis).recip();
        (0.0, quat::scale(norm_inv, axis))
    } else {
        let c = quat::normalize( quat::sub(a_u, b_u) );
        let r = orthogonal_vector(b);
        quat::mul(r, c)
    }
}

/// aに直交し，ノルムが1であるベクトルを返す．ただし norm(a) > 0 であること．
fn orthogonal_vector(a: Vector3<f32>) -> Vector3<f32> {
    let mut working_array = [0.0; 3];
    working_array[0] = a[0].abs();

    // 最大値を探す
    let mut i_max: usize = 0;
    let mut max_val = working_array[0];
    for (i, val) in a.iter().enumerate().skip(1) {
        working_array[i] = val.abs();
        if working_array[i] > max_val {
            max_val = working_array[i];
            i_max = i;
        }
    }

    // 中央値を探す
    let i_med1 = (i_max + 1) % 3;
    let i_med2 = (i_max + 2) % 3;
    let i_med = if working_array[i_med1] > working_array[i_med2] {
        i_med1
    } else {
        i_med2
    };

    let norm_inv = ( a[i_med].hypot(a[i_max]) ).recip();
    working_array[i_med] = -a[i_max] * norm_inv;
    working_array[i_max] = a[i_med] * norm_inv;
    working_array[3 - (i_max + i_med)] = 0.0;

    working_array
}